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
            return self.parent.get_bit_string("0" + bit_string)
        else:
            return self.parent.get_bit_string("1" + bit_string)


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
            bitstring += self.codebook[c]
        return bitstring

    def huffman_decode(self, bitstring):
        able_to_decode = True
        decoded_string = ""
        while able_to_decode:
            decoded_char, bitstring = self.huffman_decode_next_char(bitstring)
            if decoded_char == False:
                able_to_decode = False
                break
            decoded_string += decoded_char
        return decoded_string

    def huffman_decode_next_char(self, bitstring, code=None):
        print bitstring
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
        self.H = np.matrix("1 0 1 1 1 0 0 0 1 1 1 1 0 0 0;" +
                           "1 1 0 1 1 0 1 1 0 0 1 0 1 0 0;" +
                           "1 1 1 0 1 1 0 1 1 0 0 0 0 1 0;" +
                           "1 1 1 1 0 1 1 0 0 1 0 0 0 0 1")

        self.G = np.concatenate((np.identity(11), np.transpose(self.H[:, :-4])), axis = 1)
        self.mod2v = np.vectorize(self.mod2)

    def compute_parities(self, bits):
        p1 = np.sum(bits[:,::2])%2
        p2 = np.sum([np.sum(bits[:,k::4]) for k in range(1,3)])%2
        p3 = np.sum([np.sum(bits[:,k::8]) for k in range(2,6)])%2
        p4 = np.sum([np.sum(bits[:,k::16]) for k in range(4,12)])%2
        parities = [[p1,p2,p3,p4]]
      #  print parities
        return parities

    def encode_chunks(self, bitstring):
        chunks = chunk_bitstring(bitstring, 11)
        encoded_chunks = [self.hamming_encode(convert_string_to_intaarray(x)) for x in chunks]
        return encoded_chunks

    def decode_chunks(self, chunks):
        decoded_chunks = [self.hamming_decode(x) for x in chunks]
        return decoded_chunks

    def hamming_encode(self, bits):
        # splits = np.array_split(bits, 3, axis=1);
        # np.concatenate((splits[-1], np.zeros((1,4 -splits[-1].shape[1]))), axis = 1)

        parities = self.compute_parities(bits)
        return np.concatenate((bits, parities), axis = 1)
        #return self.mod2v(bits*self.G)
   
    def mod2(self,a): return int(a%2)

    def hamming_decode(self, code):
        self.H = np.matrix("1 0 1 0 1 0 1 0 1 0 1 1 0 1 0;"+
                            "0 1 1 0 0 1 1 0 0 1 1 0 0 1 1;"+
                            "0 0 0 1 1 1 1 0 0 0 0 1 1 1 1;"+
                            "0 0 0 0 0 0 0 1 1 1 1 1 1 1 1")

        parities = self.mod2v(self.H * np.transpose(code))
        parities2 = self.compute_parities(code[:, :-4])
        print code[:, -4:]
        print "parities:"
        print np.transpose(parities)
       # print abs(parities2 - code[:, -4:])
        print
        
      #  parities = np.transpose(abs(parities2 - code[:, -4:]))
        
        if np.sum(parities) != 0:
            index = parities[0] + 2 * parities[1] + 4 * parities[2] + 8 * parities[3]
            index = index[0,0]-1
            code[0, index] = 1 - code[0, index];
        else:
            index = -1
        return index, code[:,:-4]

        

# char_count = get_character_count(read_in_file("pg2852.txt"))
# print char_count
# code = HuffmanCode(char_count)
# encoded_string = code.huffman_encode("test")
# print code.huffman_decode(encoded_string)

hamming = HammingCode()
original = "11010110100"
bits = bitstring2matrix(original)
print
print "original message:"
print bits
print
code = hamming.hamming_encode(bits)
print "message with parity bits:"
print code
print
randombit = np.random.randint(0,15)
code[0, randombit] = 1 - code[0, randombit]
print "flipping bit " + str(randombit)
print code
print

index, output = hamming.hamming_decode(code)
if index != -1:
    print "fixed bit",
    print index
else:
    print "no errors found"


print "decoded and corrected message"
print output
print np.all(bits == output) 
print   
