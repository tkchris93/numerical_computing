from itertools import izip_longest
def partition(iterable, n, fillvalue=None):
	'''Partition data into blocks of length `n', padding with `fillvalue' if ←􏰀
	         needed. Return a list of the partitions.
	EXAMPLE:
	>>> partition('ABCDEFG', 3, 'x')
	['ABC', 'DEF', 'Gxx']
	'''
	args = [iter(iterable)] * n
	pieces = izip_longest(fillvalue=fillvalue, *args) return [''.join(block) for block in pieces]

def string_size(n):
	'''Return the maximum number of characters that can be encoded with the public key (e, n).
	In other words, find the largest integer L, such that if `string' has at most􏰀 L 
	characters, then a2i(`string') will be less than `n.'
	'''
    L=0
    max_int = 0
    while max_int < n:
        max_int += sum([2**i for i in range(8*L, 8*L+8)])
        L += 1
    return L-1

def string_to_int(msg):
	'''Convert the string `msg' to an integer.'''
	# bytearray will give us the ASCII values for each character 
	if not isinstance(msg, bytearray):
        msg = bytearray(msg)
    binmsg = []
    # convert each character to binary
    for c in msg:
        binmsg.append(bin(c)[2:].zfill(8))
	return int(''.join(binmsg), 2) 
def int_to_string(msg):
	'''Convert the integer `msg' to a string.
    	This function is the inverse of string_to_int().
	'''
    # convert to binary first
    binmsg = bin(msg)[2:]
    # we need to pad the message so length is divisible by 8
    binmsg = "0"*(8-(len(binmsg)%8)) + binmsg
    msg = bytearray()
    for block in partition(binmsg, 8):
        # convert block of 8 bits back to ASCII
        msg.append(int(block, 2))
    return str(msg)
