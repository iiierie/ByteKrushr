#include <iostream>
#include <vector>
#include <string>
using namespace std;

int window_size = 13;      // Size of the sliding window
int search_buffer = 7;     // Size of the search buffer
int look_ahead_buffer = 6; // Size of the look-ahead buffer

struct Token
{
    int offset;          // Offset of the longest match
    int length_of_match; // Length of the longest match
};

vector<Token> compression_lz77(const string& input)
{
    int inputLength = input.length();
    vector<Token> data;
    int position = 0;

    while (position < inputLength)
    {
        Token token;
        token.offset = 0;
        token.length_of_match = 0;
      
        // Calculate the maximum offset based on the search buffer
        int max_offset = (position - search_buffer) < 0 ? position : search_buffer;
      
        // Calculate the maximum search length based on the look-ahead buffer
        int max_search_length = (position + look_ahead_buffer) > inputLength ? inputLength - position : look_ahead_buffer;

        // Search for the longest match in the search buffer
        for (int offset = 1; offset <= max_offset; offset++)
        {
            int len = 0;
            while (len < max_search_length && input[position - offset + len] == input[position + len])
            {
                len++;
            }
          
            // Update the token if a longer match is found
            if (len > token.length_of_match)
            {
                token.offset = offset;
                token.length_of_match = len;
            }
        }

        data.push_back(token);
        position += token.length_of_match + 1;
    }

    return data;
}

string decompress_lz77(const vector<Token>& tokens, const string& original_input)
{
    string tmp;
    int pos = 0;
    int inputLength = original_input.length();

    for (const auto& token : tokens)
    {
        if (token.offset != 0)
        {
            int start = pos - token.offset;
            int len = token.length_of_match;
            // Copy the matched substring
            while (len > 0)
            {
                tmp += tmp[start];
                start++;
                len--;
                pos++;
            }
        }
        if (pos < inputLength) {
            tmp += original_input[pos];
            pos++;
        }
    }

    return tmp;
}

void run()
{
    string input;
    cout << "Enter Input: ";
    getline(cin, input);

    if (input.empty()) {
        cout << "Empty input. Please provide a valid input string." << endl;
        return;
    }

    auto tokens = compression_lz77(input);
    cout << "Compression:" << endl;
    cout << "<Offset, Length Of Match>: " << endl;
    for (const auto& token : tokens)
    {
        cout << "<" << token.offset << ", " << token.length_of_match << ">" << endl;
    }

    string compressed_output;
    for (size_t i = 0; i < tokens.size(); i++)
    {
        if (tokens[i].offset == 0 && tokens[i].length_of_match == 0)
        {
            compressed_output += input[i];
        }
        else
        {
            compressed_output += "<" + to_string(tokens[i].offset) + "," + to_string(tokens[i].length_of_match) + ">";
        }
    }
    
    cout << "Compressed Output: " << compressed_output << endl;
    cout << "Decompressed Output: " << decompress_lz77(tokens, input) << endl;
}

int main()
{
    run();
    return 0;
}
