## ByteKrushr - File Compression App
ByteKrushr is a Streamlit-based application for file compression using various algorithms. 


### How to Use ByteKrushr? 

1. **Select Compression Algorithm:** Choose one of the available algorithms from the sidebar.
   
2. **Select Action:** Choose whether you want to compress or decompress text.
   
3. **Upload File or Paste Text:** Upload a .txt file or paste text into the provided text area. For compression, ensure the file uploaded is a .txt file. For decompression, upload a .bin file containing previously compressed data.

4. **Execute:** Click the "Execute" button to initiate the compression or decompression process.
   
5. **View Processed Output:** After processing, the output will be displayed below. For compression, you will see the compressed data. For decompression, the decompressed text will be shown. You can also download the processed file using the "Download Processed File" button.

**Note:** 
- **Input File Types:** Upload .txt files for compression and .bin files for decompression.
- **Output File Type:** Compressed data will be saved as .bin files, and decompressed data will be shown as text in the app.


---
### **TEXT Modality**: 
You can compress and decompress text files using Huffman coding, LZW (Lempel-Ziv-Welch), DEFLATE, and LZ77 algorithms. The compressions are lossless so those compressed files can be used anytime to decompress and get back the original files.
#### Lossless Text Compresssion Algorithms Available

##### LZ77 (Lempel-Ziv 1977)
LZ77 is a sliding window compression algorithm. It replaces repeated occurrences of data with references to a single copy of that data existing earlier in the uncompressed data stream.

##### Huffman Coding
Huffman coding is a popular algorithm used for lossless data compression. It assigns variable-length codes to input characters, with shorter codes assigned to more frequently occurring characters.

##### LZW (Lempel-Ziv-Welch)
LZW is another widely used algorithm for text compression. It builds a dictionary of strings encountered in the input text and replaces the strings with codes from the dictionary to achieve compression.

##### DEFLATE
DEFLATE is a combination of LZ77 (Lempel-Ziv 1977) algorithm and Huffman coding. It's the compression algorithm used in formats such as gzip and PNG files. DEFLATE first applies LZ77 to create a sequence of literals and lengths, and then Huffman coding to compress the resulting data.


---

[TODO] : Currently, it supports text modality, but images and pdfs will be added soon.

---


**Sandesh Shrestha** | sandesh.cdr@gmail.com | [iiierie.github.io](https://iiierie.github.io)
