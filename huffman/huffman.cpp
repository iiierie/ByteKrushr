#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_map>
#include <string>
#include <functional>

using namespace std;

struct Node {
    char ch;
    int freq;
    Node *left, *right;
    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
};

struct Compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};

void buildHuffmanTree(const string& text, unordered_map<char, string>& huffmanCode) {
    unordered_map<char, int> freq;
    for (char ch : text) {
        freq[ch]++;
    }

    priority_queue<Node*, vector<Node*>, Compare> pq;
    for (auto pair : freq) {
        pq.push(new Node(pair.first, pair.second));
    }

    while (pq.size() != 1) {
        Node *left = pq.top(); pq.pop();
        Node *right = pq.top(); pq.pop();
        int sum = left->freq + right->freq;
        Node *node = new Node('\0', sum);
        node->left = left;
        node->right = right;
        pq.push(node);
    }

    Node *root = pq.top();

    function<void(Node*, string)> encode = [&](Node* root, string str) {
        if (root == nullptr) return;
        if (root->ch != '\0') {
            huffmanCode[root->ch] = str;
        }
        encode(root->left, str + "0");
        encode(root->right, str + "1");
    };

    encode(root, "");
}

string compress(const string& text, unordered_map<char, string>& huffmanCode) {
    string compressed = "";
    for (char ch : text) {
        compressed += huffmanCode[ch];
    }
    return compressed;
}

string decompress(const string& compressedText, Node* root) {
    string decompressed = "";
    Node* curr = root;
    for (char bit : compressedText) {
        curr = (bit == '0') ? curr->left : curr->right;
        if (curr->left == nullptr && curr->right == nullptr) {
            decompressed += curr->ch;
            curr = root;
        }
    }
    return decompressed;
}

int main() {
    string text;
    cout << "Enter text to compress: ";
    getline(cin, text);

    unordered_map<char, string> huffmanCode;
    buildHuffmanTree(text, huffmanCode);

    cout << "Huffman Codes:\n";
    for (auto pair : huffmanCode) {
        cout << pair.first << " " << pair.second << "\n";
    }

    string compressedText = compress(text, huffmanCode);
    cout << "\nCompressed Text: " << compressedText << "\n";

    // For decompression, we need to rebuild the Huffman tree
    priority_queue<Node*, vector<Node*>, Compare> pq;
    for (auto pair : huffmanCode) {
        Node* node = new Node(pair.first, 0);
        Node* curr = node;
        for (char bit : pair.second) {
            if (bit == '0') {
                if (!curr->left) curr->left = new Node('\0', 0);
                curr = curr->left;
            } else {
                if (!curr->right) curr->right = new Node('\0', 0);
                curr = curr->right;
            }
        }
        pq.push(node);
    }
    while (pq.size() > 1) {
        Node* left = pq.top(); pq.pop();
        Node* right = pq.top(); pq.pop();
        Node* parent = new Node('\0', 0);
        parent->left = left;
        parent->right = right;
        pq.push(parent);
    }
    Node* root = pq.top();

    string decompressedText = decompress(compressedText, root);
    cout << "\nDecompressed Text: " << decompressedText << "\n";

    return 0;
}
