window_size = 13      # Size of the sliding window
search_buffer = 7     # Size of the search buffer
look_ahead_buffer = 6 # Size of the look-ahead buffer

def compress_lz77(input_text):
    compressed_output = ""
    position = 0
    input_length = len(input_text)
    search_buffer = 13
    look_ahead_buffer = 6
    
    while position < input_length:
        token = {'offset': 0, 'length_of_match': 0}
        
        # Calculate the maximum offset based on the search buffer
        max_offset = min(position, search_buffer)
        
        # Calculate the maximum search length based on the look-ahead buffer
        max_search_length = min(input_length - position, look_ahead_buffer)
        
        # Search for the longest match in the search buffer
        for offset in range(1, max_offset + 1):
            length = 0
            while (length < max_search_length and
                   position - offset + length >= 0 and
                   input_text[position - offset + length] == input_text[position + length]):
                length += 1
            
            # Update the token if a longer match is found
            if length > token['length_of_match']:
                token['offset'] = offset
                token['length_of_match'] = length
        
        # Append the token to the compressed output
        if token['length_of_match'] > 2:
            compressed_output += f"<{token['offset']},{token['length_of_match']}>"
            position += token['length_of_match']
        else:
            compressed_output += input_text[position]
            position += 1
    
    return compressed_output


def decompress_lz77(compressed_text):
    output = []
    pos = 0
    while pos < len(compressed_text):
        if compressed_text[pos] == '<':
            temp = ''
            pos += 1
            while compressed_text[pos]!= ',':
                temp += compressed_text[pos]
                pos += 1
            offset = int(temp)
            pos += 1
            temp = ''
            while compressed_text[pos]!= '>':
                temp += compressed_text[pos]
                pos += 1
            length = int(temp)
            pos += 1
            start = len(output) - offset
            for i in range(length):
                output.append(output[start + i])
        else:
            output.append(compressed_text[pos])
            pos += 1
    return ''.join(output)

def run():
    input_text = input("Enter Input: ").strip()
    
    if not input_text:
        print("Empty input. Please provide a valid input string.")
        return
    
    tokens = compress_lz77(input_text)
    print("Compression:")
    print("<Offset, Length Of Match>: ")
    for token in tokens:
        print(f"<{token['offset']}, {token['length_of_match']}>")
    
    compressed_output = ''
    for i, token in enumerate(tokens):
        if token['offset'] == 0 and token['length_of_match'] == 0:
            compressed_output += input_text[i]
        else:
            compressed_output += f"<{token['offset']},{token['length_of_match']}>"
    
    print("Compressed Output: ", compressed_output)
    print("Decompressed Output: ", decompress_lz77(tokens, input_text))



if __name__ == "__main__":
    input_text = input("Enter Input: ").strip()
    compressed = compress_lz77(input_text)
    print(compressed)

    decompressed = decompress_lz77(compressed)
    print(decompressed)
