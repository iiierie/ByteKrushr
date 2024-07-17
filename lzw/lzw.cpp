#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>

const int DICTIONARY_SIZE = 256;

std::vector<int> compress(const std::string& input) {
    std::unordered_map<std::string, int> dictionary;
    std::vector<int> result;
    std::string temp;

    // Initialize dictionary with single character entries
    for (int i = 0; i < DICTIONARY_SIZE; ++i) {
        dictionary[std::string(1, char(i))] = i;
    }

    int dictSize = DICTIONARY_SIZE;

    for (char c : input) {
        std::string temp2 = temp + c;
        if (dictionary.find(temp2) != dictionary.end()) {
            temp = temp2;
        } else {
            result.push_back(dictionary[temp]);
            dictionary[temp2] = dictSize++;
            temp = std::string(1, c);
        }
    }

    if (!temp.empty()) {
        result.push_back(dictionary[temp]);
    }

    return result;
}

std::string decompress(const std::vector<int>& input) {
    std::unordered_map<int, std::string> dictionary;
    std::string result;

    // Initialize dictionary with single character entries
    for (int i = 0; i < DICTIONARY_SIZE; ++i) {
        dictionary[i] = std::string(1, char(i));
    }

    int dictSize = DICTIONARY_SIZE;

    std::string temp = dictionary[input[0]];
    result += temp;

    for (size_t i = 1; i < input.size(); ++i) {
        int current = input[i];
        std::string entry;

        if (dictionary.find(current) != dictionary.end()) {
            entry = dictionary[current];
        } else {
            entry = temp + temp[0];
        }

        result += entry;

        // Add entry to dictionary
        dictionary[dictSize++] = temp + entry[0];

        temp = entry;
    }

    return result;
}

int main() {
    std::string input_data;

    // Prompt user for input
    std::cout << "Enter the input string: ";
    std::getline(std::cin, input_data);

    // Compress the input data
    std::vector<int> compressed_data = compress(input_data);

    // Decompress the compressed data
    std::string decompressed_data = decompress(compressed_data);

    // Output results
    std::cout << "Original: " << input_data << std::endl;
    std::cout << "Compressed: ";
    for (int code : compressed_data) {
        std::cout << code << " ";
    }
    std::cout << std::endl;
    std::cout << "Decompressed: " << decompressed_data << std::endl;

    return 0;
}
