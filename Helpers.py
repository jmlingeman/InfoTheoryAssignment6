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


def bitstring2matrix(bitstring):
	return  np.matrix([int(x) for x in list(bitstring)])


