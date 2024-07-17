#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <cctype>
#include <memory>

#define SIZE 128

struct TreeNode {
    float frequency;
    char character;
    std::string code;
    std::unique_ptr<TreeNode> left;
    std::unique_ptr<TreeNode> right;

    TreeNode(char ch, float freq) : character(ch), frequency(freq) {}
};

void findMin(std::vector<std::unique_ptr<TreeNode>>& nodes, float& min, int& minIndex, float& secondMin, int& secondMinIndex) {
    minIndex = -1;
    secondMinIndex = -1;

    for (int i = 0; i < nodes.size(); i++) {
        if (nodes[i] && (minIndex == -1 || nodes[i]->frequency < nodes[minIndex]->frequency)) {
            minIndex = i;
        }
    }

    if (minIndex != -1) {
        min = nodes[minIndex]->frequency;
        for (int i = 0; i < nodes.size(); i++) {
            if (nodes[i] && i != minIndex && (secondMinIndex == -1 || nodes[i]->frequency < nodes[secondMinIndex]->frequency)) {
                secondMinIndex = i;
            }
        }
        if (secondMinIndex != -1) {
            secondMin = nodes[secondMinIndex]->frequency;
        }
    }
}

void encode(TreeNode* node, std::vector<std::unique_ptr<TreeNode>>& chars, char direction, int level, std::string code) {
    if (node != nullptr) {
        if (direction == 'L') {
            code += '0';
        } else if (direction == 'R') {
            code += '1';
        }
        if (std::isupper(node->character)) {
            node->code = code;
            chars[node->character - 'A']->code = code;
        }
        encode(node->left.get(), chars, 'L', level + 1, code);
        encode(node->right.get(), chars, 'R', level + 1, code);
    }
}

void traverseTree(TreeNode* node, std::string& key) {
    if (node != nullptr) {
        if (std::isupper(node->character)) {
            key += node->character;
            key += node->code;
        }
        traverseTree(node->left.get(), key);
        traverseTree(node->right.get(), key);
    }
}

struct Data {
    int offset;
    int length;
    char ch;
};

void write(const Data& result, std::ofstream& out) {
    short int shift = result.offset << 6;
    short int off_len = shift + result.length;
    out.write(reinterpret_cast<const char*>(&off_len), sizeof(off_len));
    out.write(&result.ch, sizeof(result.ch));
}

float fileSize(const std::string& fileName) {
    std::ifstream file(fileName, std::ifstream::ate | std::ifstream::binary);
    return static_cast<float>(file.tellg()) * 0.000977;
}

Data encoder(const std::string& search, const std::string& forward) {
    Data data;
    if (search.empty()) {
        data.offset = 0;
        data.length = 0;
        data.ch = forward[0];
        return data;
    }

    if (forward.empty()) {
        data.offset = -1;
        data.length = -1;
        data.ch = ' ';
        return data;
    }

    int maxMatch = 0;
    int maxDistance = 0;

    std::string combinedArray = search + forward;

    for (size_t p = 0; p < search.size(); ++p) {
        int match = 0;
        while (combinedArray[p + match] == combinedArray[search.size() + match]) {
            match++;
            if ((search.size() + match) == combinedArray.size()) {
                match--;
                break;
            }
            if ((p + match) >= search.size()) {
                break;
            }
        }
        if (match > maxMatch) {
            maxDistance = p;
            maxMatch = match;
        }
    }
    data.offset = maxDistance;
    data.length = maxMatch;
    data.ch = combinedArray[search.size() + maxMatch];
    return data;
}

void lz77encoder(const std::string& txt, const std::string& outTxt) {
    Data results;
    int x = 16;
    int maxSearch = 1024;
    int maxLH = std::pow(2, (x - (std::log2(maxSearch))));

    std::ifstream textFile(txt);
    std::ofstream outFile(outTxt, std::ios::binary);

    textFile.seekg(0, std::ios::end);
    int length = textFile.tellg();
    textFile.seekg(0, std::ios::beg);

    std::vector<char> text(length);
    textFile.read(text.data(), length);

    int searchIterator = 0;
    int forwardIterator = 0;
    int control = 0;

    while (forwardIterator < length) {
        int aI = searchIterator;
        int fI = forwardIterator;
        int bA = forwardIterator - searchIterator;
        int bI = maxLH;

        if (bI > length) {
            if (control == 0) {
                bI = length;
                control++;
            } else if (control > 0) {
                bI = length - bA;
            }
        } else if (bI <= length) {
            control++;
            if (control > 0) {
                bI = length - bA;
            }
        }

        std::string searchArray(text.begin() + aI, text.begin() + aI + bA);
        std::string forwardArray(text.begin() + fI, text.begin() + fI + bI);

        results = encoder(searchArray, forwardArray);
        write(results, outFile);

        forwardIterator = forwardIterator + results.length + 1;
        searchIterator = forwardIterator - maxSearch;

        if (searchIterator < 0) {
            searchIterator = 0;
        }
    }
}

void huffmanEncoding(const std::string& inTxt, const std::string& outTxt) {
    std::ifstream in(inTxt);
    std::ofstream out;

    std::vector<std::unique_ptr<TreeNode>> nodes(26), chars(26);
    std::string str;
    int charCount = 0;

    while (std::getline(in, str)) {
        for (char& ch : str) {
            ch = std::toupper(ch);
            if (std::isupper(ch)) {
                charCount++;
                int index = ch - 'A';
                if (!nodes[index]) {
                    nodes[index] = std::make_unique<TreeNode>(ch, 1);
                } else {
                    nodes[index]->frequency += 1;
                }
            }
        }
    }

    in.close();

    for (auto& node : nodes) {
        if (node) {
            node->frequency /= charCount;
        }
    }

    int j = 1;
    int minIndex, secondMinIndex;
    float min, secondMin;
    do {
        findMin(nodes, min, minIndex, secondMin, secondMinIndex);
        if (minIndex != -1 && secondMinIndex != -1 && minIndex != secondMinIndex) {
            auto tree = std::make_unique<TreeNode>(j++, nodes[minIndex]->frequency + nodes[secondMinIndex]->frequency);
            tree->left = std::move(nodes[minIndex]);
            tree->right = std::move(nodes[secondMinIndex]);
            nodes[minIndex] = std::move(tree);
            nodes[secondMinIndex] = nullptr;
        }
    } while (j < 26);

    std::string key = ">";
    for (auto& node : nodes) {
        if (node) {
            encode(node.get(), chars, 0, 0, "");
            traverseTree(node.get(), key);
            break;
        }
    }

    in.open(inTxt);
    out.open(outTxt);
    while (std::getline(in, str)) {
        for (char& ch : str) {
            ch = std::toupper(ch);
            if (std::isupper(ch)) {
                int index = ch - 'A';
                out << chars[index]->code;
            }
        }
    }

    out << key;
    out.close();
    in.close();
}

int main() {
    std::string file;
    std::cout << "Enter the file name with the extension: ";
    std::cin >> file;

    std::string huffmanFile = "huffman.txt";
    std::string lz77File = "lz77.txt";
    float originalSize = fileSize(file);
    float huffmanSize, lz77Size, huffmanLz77Size;

    huffmanEncoding(file, huffmanFile);
    huffmanSize = fileSize(huffmanFile);
    lz77encoder(file, lz77File);
    lz77Size = fileSize(lz77File);
    lz77encoder(huffmanFile, "huffman_lz77.txt");
    huffmanLz77Size = fileSize("huffman_lz77.txt");

    std::cout << "Original File Size: " << originalSize << " KB" << std::endl;
    std::cout << "Compressed with Huffman Size: " << huffmanSize << " KB" << std::endl;
    std::cout << "Compressed with LZ77 Size: " << lz77Size << " KB" << std::endl;
    std::cout << "Compressed with Huffman and LZ77 Size: " << huffmanLz77Size << " KB" << std::endl;

    return 0;
}
