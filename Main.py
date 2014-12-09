__author__ = 'jesse'

from Coding import *
from Channel import *


# Read in the text, create the Huffman Code
book = read_in_file("pg2852.txt")
# book = ["aaaabbbccd"]
char_count = get_character_count(book)
map_to_latex_table(char_count)
huffman_code = HuffmanCode(char_count)

# Convert the book text to ASCII bits
ascii_bitstring = convert_ascii_to_binary("".join(book))
print "".join(book)

# Send the ascii bitstring thru the channel
channel = Channel()
# corrupted_bitstring = channel.binary_symmetric_channel(ascii_bitstring, perror=0.02)
# corrupted_string = "".join([convert_binary_to_ascii(x) for x in chunk_bitstring("".join(corrupted_bitstring), 8)])
# print corrupted_string
hamming = HammingCode()

# a = hamming.decode_chunks(hamming.encode_chunks(ascii_bitstring))
# print book
# print ascii_bitstring
# print chunk_bitstring("".join(ascii_bitstring), 8)
# for c in chunk_bitstring("".join(ascii_bitstring), 8):
# print c, convert_binary_to_ascii(c)
# print "".join([convert_binary_to_ascii(x) for x in chunk_bitstring("".join(ascii_bitstring), 7)])
# sys.exit(0)

# Now use the hamming coder to send it with error correction and ascii

print "Sending ascii bitstring over channel"
channel.reset()
hamming_ascii = hamming.encode_chunks(ascii_bitstring)
hamming_corrupted_bitstring = channel.binary_symmetric_channel(hamming_ascii, perror=0.02)
print "Decoding ascii bitstring"
hamming_decoded_ascii = hamming.decode_chunks(hamming_corrupted_bitstring)
# print "TOTAL ERRORS DETECTED: ", hamming.errors
hamming_ascii_final = "".join([convert_binary_to_ascii(x) for x in chunk_bitstring("".join(hamming_decoded_ascii), 8)])
# print hamming_ascii_final

print "A. NUM CHARS IN DOC: ", len("".join(book))
print "B. BINARY CHARS IN DOC: ", len(ascii_bitstring)
print "C. NUM ERRORS FROM CHANNEL: ", channel.num_errors
print "D. NUM NO ERRORS FROM CHANNEL: ", channel.no_errors
print "E. NUM CODEWORDS 1 ERR: ", channel.one_errors
print "F. NUM CODEWORDS 2 ERR: ", channel.double_errors
print "G. MORE THAN 2 ERRORS: ", channel.more_than_double_errors
print "H. BIT ERRORS AFTER DECODE: ", count_string_differences("".join(hamming_decoded_ascii), ascii_bitstring)
print "I. CODEWORD ERRORS AFTER DECODE: ", sum(
    [1 if x != y else 0 for x, y in zip(chunk_bitstring(ascii_bitstring, 11), hamming_decoded_ascii)])

print "J. CHARACTERS WRONG: ", count_string_differences(hamming_ascii_final, "".join(book))

print "NUM STRINGS SENT: ", channel.strings_sent
bits_sent = channel.strings_sent * 15
print "EXPECTED CODEWORDS WITH 1 ERROR: ", bits_sent * 0.02 / 15
print "EXPECTED CODEWORDS WITH 2 ERRORS: ", bits_sent * 0.02 * 0.02 / 15
print "UPPER BOUND ON CODEWORDS WITH MORE THAN 2 ERRORS: ", bits_sent * 0.02 * 0.02 * 0.02 / 15

# print "NUM CODEWORDS 0 ERRORS: ", hamming.no_errors
# print "NUM CODEWORDS 1 ERROR: ", hamming.errors
# print "COUNT OF UNCOMPRESSED ERRORS: ", count_string_differences()

# print hamming_ascii_final

channel.reset()

# Now do the same thing but with Huffman Coding
print "Encoding Huffman"
huffman_string = huffman_code.huffman_encode("".join(book))

print "Decoding Huffman"
# huffman_code.huffman_decode(huffman_string)

hamming_huffman = hamming.encode_chunks(huffman_string)
hamming_huffman_corrupted_bitstring = channel.binary_symmetric_channel(hamming_huffman, perror=0.02)
hamming_decoded_huffman = hamming.decode_chunks(hamming_huffman_corrupted_bitstring)
successful_decoding, hamming_huffman_final = huffman_code.huffman_decode("".join(hamming_decoded_huffman))
# print hamming_huffman_final
print "HAMMING DECODE SUCCESSFUL: ", successful_decoding
print "TOTAL ERRORS DETECTED: ", hamming.errors

print "COMPRESSION FACTOR: ", float(len(ascii_bitstring)) / len(huffman_string)
print "HUFFMAN CHARACTERS WRONG: ", count_string_differences(hamming_huffman_final, "".join(book))


