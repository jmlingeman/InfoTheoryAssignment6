from Queue import PriorityQueue
from Helpers import *

__author__ = 'jesse'


class Node:

    def __init__(self, freq, char, children):
        self.freq = freq
        self.char = char
        self.children = children
        self.parent = None

    def __cmp__(self, other):
        return self.freq - other.freq

    def combine(self, other):
        return Node(self.freq + other.freq, "", sorted([self, other]))

    def get_bit_string(self, bit_string):
        if self.parent is None:
            return bit_string

        if self.parent.children[0] == self:
            return self.parent.get_bit_string(bit_string + "0")
        else:
            return self.parent.get_bit_string(bit_string + "1")


class HuffmanCode:

    def __init__(self, char_count):
        self.char_count = char_count
        self.code, self.leaf_nodes = self.build_huffman_code()
        self.codebook = self.convert_code_to_dict(self.code)
        print(self.codebook)

    def get_min_node(self, q1, q2):
        if not q1.empty() and q2.empty():
            return q1.get()
        elif q1.empty() and not q2.empty():
            return q2.get()
        elif q1.queue[0] < q2.queue[0]:
            return q1.get()
        else:
            return q2.get()

    def convert_code_to_dict(self, code):
        codebook = {}
        for node in self.leaf_nodes:
            codebook[node.char] = node.get_bit_string("")
        return codebook



    def build_huffman_code(self):
        sorted_characters = sorted(self.char_count.items(), key=lambda(k, v): (v, k))

        # We need to flip the tuples for the priority queue
        leaf_nodes = [Node(x[1], x[0], []) for x in sorted_characters]

        initial = PriorityQueue()
        combined = PriorityQueue()

        for x in leaf_nodes:
            initial.put(x)

        while len(initial.queue) > 0 or len(combined.queue) > 1:
            n1 = self.get_min_node(initial, combined)
            n2 = self.get_min_node(initial, combined)

            print "Got {0} and {1}".format(n1.char, n2.char)

            new_node = n1.combine(n2)
            n1.parent = new_node
            n2.parent = new_node
            combined.put(new_node)

        return combined.get(), leaf_nodes

    def huffman_encode(self, s):
        bitstring = ""
        for c in s:
            bitstring += self.codebook[s]

    def huffman_decode(self, s):
        pass


class HammingCode:
    def __init__(self):
        NotImplementedError

    def HammingEncode(self, bitstring):
        NotImplementedError

    def HammingDecode(self, bitstring):
        NotImplementedError


# char_count = get_character_count(read_in_file("pg2852.txt"))
# print char_count
# code = HuffmanCode(char_count)