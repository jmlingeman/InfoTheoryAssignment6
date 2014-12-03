__author__ = 'jesse'
import random


class Channel:
    def binary_symmetric_channel(self, chunks, perror=0.02):
        corrupted_chunks = []
        for chunk in chunks:
            corrupted_string = ""
            for c in chunk:
                if random.random() < perror:
                    corrupted_string += "0" if c == "1" else "1"
                else:
                    corrupted_string += c
            corrupted_chunks.append(corrupted_string)

        return corrupted_chunks