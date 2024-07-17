
### Compression

Assuming you have a file `input.txt` that you want to compress into `compressed.pkl`:

```bash
python compression\lzw_text_compression\lzw.py compress -i compression\lzw_text_compression\examples\input.txt -o compression\lzw_text_compression\examples\compressed.pkl
```

- `-i input.txt`: Specifies the input file (`input.txt`) to compress.
- `-o compressed.pkl`: Specifies the output file (`compressed.pkl`) where compressed data will be saved.

### Decompression

Assuming you have a compressed file `compressed.pkl` that you want to decompress into `output.txt`:

```bash
python compression\lzw_text_compression\lzw.py decompress -i compression\lzw_text_compression\examples\compressed.pkl -o compression\lzw_text_compression\examples\decompressed.txt
```

- `-i compressed.pkl`: Specifies the input file (`compressed.pkl`) containing compressed data.
- `-o output.txt`: Specifies the output file (`output.txt`) where decompressed data will be saved.

### Explanation

- **Usage**: Replace `input.txt` and `compressed.pkl` with your actual file paths and filenames. Adjust paths as necessary based on where your script (`lzw.py`) and files are located.

- **Commands**: Run these commands in your terminal or command prompt where Python is installed and accessible. Ensure you have the appropriate permissions to read from and write to the specified files and directories.

By following these instructions, you can effectively compress and decompress files using the LZW implementation provided in your `lzw.py` script.