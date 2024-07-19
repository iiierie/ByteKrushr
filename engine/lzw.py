def compress_lzw(input_data):
    # Initialize the dictionary with ASCII characters (0-255)
    dictionary = {chr(i): i for i in range(256)}
    result = []
    temp = ""

    for c in input_data:
        temp2 = temp + c
        if temp2 in dictionary:
            temp = temp2
        else:
            try:
                result.append(dictionary[temp])
            except KeyError:
                # Handle the KeyError by skipping or adding a default value
                print(f"Skipping unknown character sequence: {temp}")
                # You might want to add some logic here for handling the error
                temp = c  # Reset temp to current character
                continue  # Skip adding the result for this sequence
            dictionary[temp2] = len(dictionary)
            temp = c

    if temp:
        try:
            result.append(dictionary[temp])
        except KeyError:
            # Handle the KeyError by skipping or adding a default value
            print(f"Skipping final unknown character sequence: {temp}")

    resultstring = ' '.join([str(elem) for elem in result])
    return resultstring


def decompress_lzw(compressed_data_string):
    compressed_data = [int(elem) for elem in compressed_data_string.split()]
    dictionary = {i: chr(i) for i in range(256)}
    result = []
    sequence = compressed_data[:]
    current_code = sequence.pop(0)
    result.append(dictionary[current_code])

    w = dictionary[current_code]

    for k in sequence:
        if k in dictionary:
            entry = dictionary[k]
        elif k == len(dictionary):
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k %s' % k)

        result.append(entry)
        dictionary[len(dictionary)] = w + entry[0]
        w = entry

    return ''.join(result)


# # Example usage:
# if __name__ == "__main__":
#     # Example of compressing data
#     text = """
# In conclusion, anime embodies a rich tapestry of artistic expression, cultural heritage, and storytelling innovation that resonates with audiences worldwide."""
    
#     compressed_data = compress_lzw(text)
#     print("Compressed:", compressed_data)

#     # Example of decompressing data
#     decompressed_data = decompress_lzw(compressed_data)
#     print("Decompressed:", decompressed_data)
