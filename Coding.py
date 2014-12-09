from Queue import PriorityQueue

from Helpers import *


__author__ = 'jesse'


class Node:
    def __init__(self, freq, char, children):
        self.freq = freq
        self.char = char
        self.children = children
        self.parent = None
        for n in children:
            n.parent = self

    def __cmp__(self, other):
        return self.freq - other.freq

    def combine(self, other):
        return Node(self.freq + other.freq, "", sorted([self, other]))

    def get_bit_string(self, bit_string):
        if self.parent is None:
            # print "---------"
            return bit_string

        # if self.char == "b":
        # print self.parent

        if self.parent.children[0] is self:
            # print "GOING LEFT FOR " + self.char
            return self.parent.get_bit_string("0" + bit_string)
        elif self.parent.children[1] is self:
            # print "GOING RIGHT FOR " + self.char
            return self.parent.get_bit_string("1" + bit_string)
        else:
            print "ERROR"

    def __repr__(self):
        return "\nChar: {0}, Freq: {1}, Parent: {2}, Children: {3}".format(self.char, self.freq, (
        self.parent.char, self.parent.freq) if self.parent is not None else None, self.children)


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
        sorted_characters = sorted(self.char_count.items(), key=lambda (k, v): (v, k))

        # We need to flip the tuples for the priority queue
        leaf_nodes = [Node(x[1], x[0], []) for x in sorted_characters]

        initial = PriorityQueue()
        combined = PriorityQueue()

        for x in leaf_nodes:
            initial.put(x)

        while len(initial.queue) > 0 or len(combined.queue) > 1:
            n1 = self.get_min_node(initial, combined)
            n2 = self.get_min_node(initial, combined)

            # print "Got {0} and {1}".format(n1.char, n2.char)

            new_node = n1.combine(n2)
            n1.parent = new_node
            n2.parent = new_node
            combined.put(new_node)

        root = combined.get()
        # print root
        return root, leaf_nodes

    def huffman_encode(self, s):
        bitstring = ""
        for c in s:
            bitstring += self.codebook[c]
        return bitstring

    def huffman_decode(self, bitstring):
        able_to_decode = True
        decoded_string = ""
        while able_to_decode:
            decoded_char, bitstring = self.huffman_decode_next_char(bitstring)
            if decoded_char is False:
                able_to_decode = False
                break
            decoded_string += decoded_char
        return able_to_decode, decoded_string

    def huffman_decode_next_char(self, bitstring, code=None):
        # print bitstring
        if code is None:
            code = self.code
        if len(code.char) > 0:
            return code.char, bitstring
        else:
            if len(bitstring) == 0:
                return False, False
            if bitstring[0] == "0":
                # print "TAKING 0 PATH", code.children[0].char
                return self.huffman_decode_next_char(bitstring[1:], code=code.children[0])
            else:
                # print "TAKING 1 PATH", code.children[0].char
                return self.huffman_decode_next_char(bitstring[1:], code=code.children[1])


class HammingCode:
    def __init__(self):
        self.errors = 0
        self.no_errors = 0

    def compute_parities(self, bits):
        p1 = np.sum(bits[::2]) % 2
        # print bits
        p2 = (bits[2] + bits[5] + bits[6] + bits[9] + bits[10] + bits[13] + bits[14]) % 2
        # p2 = np.sum([np.sum(bits[k::5]) for k in range(1,3)]) % 2
        # p3 = np.sum([np.sum(bits[k::8]) for k in range(3,7)]) % 2
        p3 = (np.sum(bits[3:7]) + np.sum(bits[11:15])) % 2
        # p4 = np.sum([np.sum(bits[k::16]) for k in range(7,15)]) % 2
        p4 = np.sum(bits[8:15]) % 2
        parities = [p1, p2, p3, p4]

        return parities

    def encode_chunks(self, bitstring):
        chunks = chunk_bitstring(bitstring, 11)
        encoded_chunks = [self.hamming_encode(convert_string_to_intaarray(x)) for x in chunks]
        return encoded_chunks

    def decode_chunks(self, chunks):
        decoded_chunks = [self.hamming_decode(x) for x in chunks]
        return decoded_chunks

    def hamming_encode(self, bits):
        # insert parity slots
        # print bits
        bits = np.insert(bits, 0, 0)
        bits = np.insert(bits, 1, 0)
        bits = np.insert(bits, 3, 0)
        bits = np.insert(bits, 7, 0)

        #calculate parity values        
        parities = self.compute_parities(bits)

        #put values in slots
        bits[0] = parities[0]
        bits[1] = parities[1]
        bits[3] = parities[2]
        bits[7] = parities[3]

        #convert to string
        # print bits
        bits = ''.join(str(x) for x in bits)
        return bits

    def hamming_decode(self, code):

        assert (len(code) == 15)

        code = convert_string_to_intaarray(code)

        # print code

        # make copy of code
        expected = np.copy(code)

        #reset parity bits
        expected[0] = 0
        expected[1] = 0
        expected[3] = 0
        expected[7] = 0

        #recompute parity bits
        parities = self.compute_parities(expected)
        expected[0] = parities[0]
        expected[1] = parities[1]
        expected[3] = parities[2]
        expected[7] = parities[3]

        expectedparities = np.array((expected[0], expected[1], expected[3], expected[7]))
        actualparities = np.array((code[0], code[1], code[3], code[7]))


        #create a difference array
        diff = abs(expectedparities - actualparities)

        if sum(diff) != 0:
            # compute index by adding up parity bit values
            self.errors += 1
            index = diff[0] + 2 * diff[1] + 4 * diff[2] + 8 * diff[3] - 1
            code[index] = 1 - code[index]
        else:
            self.no_errors += 1
            index = -1

        #form result without parity bits
        result = [code[2]] + code[4:7] + code[8:]
        # result = np.array(result)[0]

        #convert result to string
        result = ''.join(str(x) for x in result)
        assert (len(result) == 11)
        return result


# char_count = get_character_count(read_in_file("pg2852.txt"))
# print char_count
# code = HuffmanCode(char_count)
# encoded_string = code.huffman_encode("test")
# print code.huffman_decode(encoded_string)

# hamming = HammingCode()
# original = ''.join(str(np.random.randint(0, 2)) for x in xrange(11)) 
# bits = bitstring2matrix(original)
# print
# print "original message:"
# print bits
# print
# code = hamming.hamming_encode(bits)
# print "message with parity bits:"
# print code
# print
# randombit = np.random.randint(0,15)
# code[0, randombit] = 1 - code[0, randombit]
# print "flipping bit " + str(randombit)
# print code
# print

# index, output = hamming.hamming_decode(code)
# if index != -1:
# print "fixed bit",
#     print index
# else:
#     print "no errors found"


# print "decoded and corrected message"
# print output
# print np.all(bits == output) 
#print   
