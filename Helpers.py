import binascii

import numpy as np


__author__ = 'jesse'

def read_in_file(filename):
    return open(filename, 'r').readlines()

def get_character_count(lines):
    char_count = {}
    for line in lines:
        for c in line:
            if c not in char_count:
                char_count[c] = 0
            char_count[c] += 1

    return char_count


def convert_ascii_to_binary(input_str):
    # Strip off the 0b at the start of this string with the slice at the end
    return bin(int(binascii.hexlify(input_str), 16))[2:]


def convert_binary_to_ascii(bitstring):
    n = int("0b" + bitstring, 2)
    return binascii.unhexlify('%x' % n)


def bitstring2matrix(bitstring):
    return np.matrix([int(x) for x in list(bitstring)])


def chunk_bitstring(bitstring, chunk_size):
    number_of_chunks = len(bitstring) / chunk_size
    chunks = []
    for i in range(number_of_chunks):
        chunks.append(bitstring[i * chunk_size:(i + 1) * chunk_size])
    return chunks


def convert_string_to_intaarray(s):
    return [int(x) for x in s]


def convert_intarry_to_string(intarray):
    return [str(x) for x in intarray]