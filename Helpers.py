import binascii
import re

import numpy as np


__author__ = 'jesse'

pattern = re.compile('([^\s\w]|_)+')


def read_in_file(filename):
    return map(strip_chars, open(filename, 'r').readlines())

def get_character_count(lines):
    char_count = {}
    for line in lines:
        for c in line:
            if c not in char_count:
                char_count[c] = 0
            char_count[c] += 1

    return char_count


def map_to_latex_table(table):
    from tabulate import tabulate

    print tabulate(table.items(), ["Character", "Frequency"], tablefmt="latex")


def strip_chars(line):
    return pattern.sub('', line)


def convert_ascii_to_binary(input_str):
    # Strip off the 0b at the start of this string with the slice at the end
    return "0" + bin(int(binascii.hexlify(input_str), 16))[2:]


def count_string_differences(s1, s2):
    diffs = 0
    for x, y in zip(s1, s2):
        if x != y:
            diffs += 1
    return diffs


def convert_15_bit_code_to_11(code):
    return [code[2]] + code[4:7] + code[8:]


def convert_binary_to_ascii(bitstring):
    # print bitstring
    n = int("".join(bitstring), 2)
    # print bitstring, n, '%x' % n
    # try:

    return binascii.unhexlify('%02x' % n)
    # except:
    # return "DecodingError"


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