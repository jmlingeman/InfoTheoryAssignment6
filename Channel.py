__author__ = 'jesse'
import random


class Channel:
    def __init__(self):
        self.num_errors = 0
        self.double_errors = 0
        self.strings_sent = 0
        self.no_errors = 0
        self.one_errors = 0
        self.more_than_double_errors = 0

    def binary_symmetric_channel(self, chunks, perror=0.02):
        corrupted_chunks = []
        for chunk in chunks:
            corrupted_string = ""
            num_err_in_chunk = 0
            for c in chunk:
                if random.random() < perror:
                    self.num_errors += 1
                    corrupted_string += "0" if c == "1" else "1"

                    num_err_in_chunk += 1
                else:
                    corrupted_string += c
                    # self.no_errors += 1
            self.strings_sent += 1
            corrupted_chunks.append(corrupted_string)

            if num_err_in_chunk == 1:
                self.one_errors += 1
            elif num_err_in_chunk == 2:
                self.double_errors += 1
            elif num_err_in_chunk == 0:
                self.no_errors += 1
            else:
                self.more_than_double_errors += 1


        return corrupted_chunks

    def reset(self):
        self.num_errors = 0
        self.double_errors = 0
        self.strings_sent = 0
        self.no_errors = 0
        self.one_errors = 0
        self.more_than_double_errors = 0