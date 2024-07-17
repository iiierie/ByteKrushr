import argparse
import os
import pickle
from collections import defaultdict

class Token:
    def __init__(self, offset, length_of_match):
        self.offset = offset
        self.length_of_match = length_of_match

def compression_lz77(input_data):
    input_length = len(input_data)
    data = []
    position = 0

    while position < input_length:
        token = Token(0, 0)
        
        max_offset = min(position, 13)
        max_search_length = min(input_length - position, 6)

        for offset in range(1, max_offset + 1):
            length = 0
            while (length < max_search_length and
                   input_data[position - offset + length] == input_data[position + length]):
                length += 1
            
            if length > token.length_of_match:
                token.offset = offset
                token.length_of_match = length
        
        data.append(token)
        position += token.length_of_match + 1

    return data

def decompress_lz77(tokens, input_data):
    output = bytearray()
    pos = 0
    input_data_bytes = input_data.encode()  # Convert string to bytes
    while pos < len(input_data_bytes):
        if input_data_bytes[pos] == ord('<'):
            pos += 1
            temp = bytearray()
            while input_data_bytes[pos]!= ord('>'):
                temp.append(input_data_bytes[pos])
                pos += 1
            pos += 1
            token_str = temp.decode()
            offset, length = map(int, token_str.split(','))
            start = len(output) - offset
            end = start + length
            output.extend(output[start:end])
        else:
            output.append(input_data_bytes[pos])  # Append byte to output
            pos += 1
    
    return bytes(output)



def build_huffman_tree(text):
    freq = defaultdict(int)
    for ch in text:
        freq[ch] += 1

    pq = []
    for ch, f in freq.items():
        pq.append(Node(ch, f))

    while len(pq) > 1:
        pq.sort(key=lambda x: x.freq)
        left = pq.pop(0)
        right = pq.pop(0)
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        pq.append(parent)

    return pq[0]

class Node:
    def __init__(self, ch, freq):
        self.ch = ch
        self.freq = freq
        self.left = None
        self.right = None

def encode(root):
    huffman_code = {}

    def _encode(node, code):
        if node:
            if node.ch is not None:
                huffman_code[node.ch] = code
            _encode(node.left, code + '0')
            _encode(node.right, code + '1')

    _encode(root, '')
    return huffman_code

def compress_huffman(input_data):
    root = build_huffman_tree(input_data)
    huffman_code = encode(root)

    # Convert input data to compressed binary data
    compressed_data = ''.join(huffman_code[ch] for ch in input_data)

    # Store the Huffman tree along with the compressed data
    return pickle.dumps((root, compressed_data))

def decompress_huffman(compressed_data):
    # Load the Huffman tree and compressed data
    root, compressed_data = pickle.loads(compressed_data)

    if isinstance(compressed_data, bytes):  # Check if compressed_data is bytes
        compressed_data = compressed_data.decode('utf-8')  # Decode bytes to string

    decompressed_data = []
    current = root

    for bit in compressed_data:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:
            decompressed_data.append(current.ch)
            current = root  # Reset to root for next character

    return ''.join(decompressed_data)

def compress_deflate(input_data):
    # Step 1: LZ77 Compression
    tokens = compression_lz77(input_data)
    compressed_lz77 = []
    pos = 0
    for token in tokens:
        if token.offset == 0 and token.length_of_match == 0:
            compressed_lz77.append(input_data[pos])
            pos += 1
        else:
            if token.length_of_match >= 3:
                compressed_lz77.append('<' + str(token.offset) + ',' + str(token.length_of_match) + '>')
                compressed_lz77.append(input_data[pos + token.length_of_match])
            else:
                compressed_lz77.append(input_data[pos:pos + token.length_of_match + 1])
            pos += token.length_of_match + 1

    # Step 2: Huffman Compression
    compressed_data = compress_huffman(''.join(compressed_lz77))

    return compressed_data

def decompress_deflate(compressed_data):
    # Step 1: Huffman Decompression
    decompressed_lz77 = decompress_huffman(compressed_data)

    # Step 2: LZ77 Decompression
    tokens = []
    temp = bytearray()
    pos = 0
    while pos < len(decompressed_lz77):
        if decompressed_lz77[pos] == ord('<'):
            temp = bytearray()
            pos += 1
            while decompressed_lz77[pos] != ord('>'):
                temp.append(decompressed_lz77[pos])
                pos += 1
            pos += 1
            token_str = temp.decode()
            offset, length = map(int, token_str.split(','))
            tokens.append(Token(offset, length))
        else:
            tokens.append(Token(0, 0))
            pos += 1

    decompressed_data = decompress_lz77(tokens, decompressed_lz77)

    return decompressed_data

# def run(input_file, output_file, action):
#     if action == 'compress':
#         with open(input_file, 'r') as f:
#             input_data = f.read()

#         if not input_data:
#             print("Empty input. Please provide a valid input file.")
#             return

#         compressed_data = compress_deflate(input_data)

#         with open(output_file, 'wb') as f:
#             f.write(compressed_data)

#         print("Compressed Output saved to:", output_file)

#     elif action == 'decompress':
#         with open(input_file, 'rb') as f:
#             compressed_data = f.read()

#         if not compressed_data:
#             print("Empty input. Please provide a valid input file.")
#             return

#         decompressed_data = decompress_deflate(compressed_data)

#         with open(output_file, 'wb') as f:  # Open in binary mode
#             f.write(decompressed_data)

#         print("Decompressed Output saved to:", output_file)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='DEFLATE Compression and Decompression')
#     parser.add_argument('action', choices=['compress', 'decompress'], help="Define action to be performed: compress or decompress")
#     parser.add_argument('-i', action='store', dest='input', required=True, help='Path to the Input file')
#     parser.add_argument('-o', action='store', dest='output', required=True, help='Path where to generate the Output file')
#     args = parser.parse_args()

#     run(args.input, args.output, args.action)

