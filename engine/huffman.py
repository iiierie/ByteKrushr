import os
import pickle
from collections import defaultdict

DICTIONARY_SIZE = 256

class Node:
    def __init__(self, ch, freq):
        self.ch = ch
        self.freq = freq
        self.left = None
        self.right = None

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
