import os
import pickle

DICTIONARY_SIZE = 256

def compress(input):
    global DICTIONARY_SIZE
    dictionary = {}
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(chr(i))] = i

    for c in input:
        temp2 = temp + str(chr(c))
        if temp2 in dictionary.keys():
            temp = temp2
        else:
            result.append(dictionary[temp])
            dictionary[temp2] = DICTIONARY_SIZE
            DICTIONARY_SIZE += 1
            temp = "" + str(chr(c))

    if temp != "":
        result.append(dictionary[temp])

    return result

def decompress(input):
    global DICTIONARY_SIZE
    dictionary = {}
    result = []

    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(chr(i))

    previous = chr(input[0])
    input = input[1:]
    result.append(previous)

    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous + previous[0]

        result.append(aux)
        dictionary[DICTIONARY_SIZE] = previous + aux[0]
        DICTIONARY_SIZE += 1
        previous = aux

    return result

if __name__ == "__main__":
    ABSOLUTE_PATH = os.getcwd()

    # Access arguments from args.py
    from args import arguments

    if arguments.action == 'compress':
        input_data = open(ABSOLUTE_PATH + "//" + arguments.input, "rb").read()
        output_file = open(ABSOLUTE_PATH + "//" + arguments.output, "wb")

        compressed_data = compress(input_data)
        pickle.dump(compressed_data, output_file)
    else:
        input_data = pickle.load(open(ABSOLUTE_PATH + "//" + arguments.input, "rb"))
        output_file = open(ABSOLUTE_PATH + "//" + arguments.output, "w", encoding='utf-8') 

        uncompressed_data = decompress(input_data)
        for line in uncompressed_data:
            output_file.write(line)

        output_file.close()
