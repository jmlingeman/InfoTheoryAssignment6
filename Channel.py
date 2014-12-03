__author__ = 'jesse'
import random


class Channel:
    def BSC(self, bitstring, perror=0.02):
        corrupted_string = ""
        for c in bitstring:
            if random.random() < perror:
                corrupted_string += "0" if c == "1" else "1"
            else:
                corrupted_string += c
        return corrupted_string