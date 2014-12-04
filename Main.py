__author__ = 'jesse'

from Coding import *
from Channel import *


# Read in the text, create the Huffman Code
book = read_in_file("pg2852.txt")
char_count = get_character_count(book)
huffman_code = HuffmanCode(char_count)

# Convert the book text to ASCII bits
ascii_bitstring = convert_ascii_to_binary("".join(book))

# Send the ascii bitstring thru the channel
channel = Channel()
# corrupted_bitstring = channel.binary_symmetric_channel(ascii_bitstring, perror=0.02)
# corrupted_string = convert_binary_to_ascii(corrupted_bitstring)

# Now use the hamming coder to send it with error correction and ascii
hamming = HammingCode()
hamming_ascii = hamming.encode_chunks(ascii_bitstring)
hamming_corrupted_bitstring = channel.binary_symmetric_channel(hamming_ascii, perror=0.02)
hamming_decoded_ascii = hamming.decode_chunks(hamming_corrupted_bitstring)
hamming_ascii_final = [convert_binary_to_ascii(x) for x in hamming_decoded_ascii]

# Now do the same thing but with Huffman Coding
huffman_string = huffman_code.huffman_encode("".join(book))
hamming_huffman = hamming.encode_chunks(huffman_string)
hamming_huffman_corrupted_bitstring = channel.binary_symmetric_channel(hamming_huffman, perror=0.02)
hamming_decoded_huffman = hamming.decode_chunks(hamming_huffman_corrupted_bitstring)
hamming_huffman_final = convert_binary_to_ascii(hamming_decoded_huffman)
