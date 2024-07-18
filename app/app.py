import streamlit as st
import os
import pickle
from collections import defaultdict

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine')))

from huffman import compress_huffman, decompress_huffman
from deflate import compress_deflate, decompress_deflate
from lz77 import compress_lz77, decompress_lz77
from lzw import compress_lzw, decompress_lzw

# Set page configuration
st.set_page_config(
    page_title="ByteKrushr",
    page_icon=":shark:",
    layout="wide",  # Wide layout with sidebar
    initial_sidebar_state="expanded",  # Sidebar expanded by default
)

# Sidebar
st.sidebar.title('Compression Options')
algorithm = st.sidebar.selectbox('Select Compression Algorithm', ('LZ77', 'LZW', 'DEFLATE', 'Huffman'))
action = st.sidebar.selectbox('Select Action', ('Compress', 'Decompress'))


show_readme = st.sidebar.checkbox('How to use ByteKrushr? 🦈')

if show_readme:
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        st.title('Hey there!! 😁')
        st.markdown(readme_content)  # Display Markdown content
    except Exception as e:
        st.error(f"Error reading README.md: {str(e)}")
else:
            
    # Main content
    st.title('ByteKrushr')

    # Upload file or paste text
    st.subheader('Upload File or Paste some Text ')
    uploaded_file = st.file_uploader("Choose a .txt file", type=['txt', 'bin'])
    text = st.text_area("Or paste your text here", "")

    if uploaded_file is not None:
        file_content = uploaded_file.read()
        if action == 'Compress' and uploaded_file.name.endswith('.txt'):
            text = file_content.decode('utf-8')
            st.text_area("Uploaded file content", text, height=200)  # Display in a scrollable text area
        elif action == 'Decompress' and uploaded_file.name.endswith('.bin'):
            text = file_content
            st.write("Uploaded binary content (decompression mode):")

    if st.button('Execute'):
        if not text:
            st.error("Please upload a file or paste text to process.")
        else:
            st.write(f"Selected algorithm: {algorithm}")
            st.write(f"Selected action: {action}")

            if algorithm == 'Huffman':
                if action == 'Compress':
                    output_data = compress_huffman(text)
                else:
                    output_data = decompress_huffman(text)

            elif algorithm == 'LZW':
                if action == 'Compress':
                    output_data = compress_lzw(text)
                else:
                    output_data = decompress_lzw(text)

            elif algorithm == 'DEFLATE':
                if action == 'Compress':
                    output_data = compress_deflate(text)
                else:
                    output_data = decompress_deflate(text)
            elif algorithm == 'LZ77':
                if action == 'Compress':
                    output_data = compress_lz77(text)
                else:
                    output_data = decompress_lz77(text)

            st.write("Process complete.")
            
            # Display processed data
            st.subheader('Processed Output')
            if action == 'Compress':
                if isinstance(output_data, bytes):
                    output_data_str = str(output_data)
                else:
                    output_data_str = output_data
                st.text_area('Processed Text', output_data_str, height=200)
            else:
                st.text_area('Processed Text', output_data, height=200)

            # Prepare for download
            if action == 'Compress':
                file_extension = 'bin'
                mime_type = 'application/octet-stream'
                output_data_bytes = output_data if isinstance(output_data, bytes) else output_data.encode('utf-8')
            else:
                file_extension = 'txt'
                mime_type = 'text/plain'
                output_data_bytes = output_data.encode('utf-8')

            # Download link
            st.subheader('Download Processed File')
            st.download_button(
                label='Download Processed File',
                data=output_data_bytes,
                file_name=f'processed_output.{file_extension}',
                mime=mime_type
            )
