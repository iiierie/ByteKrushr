DEFLATE is a combination of LZ77 (Lempel-Ziv 1977) and Huffman coding.

LZ77 Compression:
- Finds repeated sequences of data and replaces them with references to a previous occurrence.
- Uses a sliding window for searching and a look-ahead buffer for matching.

Huffman Coding:

- Generates a variable-length code table based on the frequency of each symbol (in this case, bytes).
- More frequent symbols get shorter codes, optimizing the overall compressed size.


