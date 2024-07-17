import argparse

parser = argparse.ArgumentParser(description='Text compressor and decompressor.')
parser.add_argument('action', choices={"compress", "decompress"}, help="Define action to be performed: compress or decompress.")
parser.add_argument('-i', action='store', dest='input', required=True, help='Path to the Input file.')
parser.add_argument('-o', action='store', dest='output', required=True, help='Path where to generate the Output file.')
arguments = parser.parse_args()
