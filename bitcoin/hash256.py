"""
* pad to original message so it length is multiple of 512
* parse original message to multiple blocks of 512 bits
* start from initial fixed has value
* doing compression function on original message block
"""

# compress function --------------------------------------------

"""
exclusive operation 
	- output is 1 if one if input is 1
"""
def demo_exclusive():
	print('demo exclusive operation')
	a = 10
	b = 9
	print(bin(a))
	print(bin(b))
	print(bin(a ^ b))

# demo_exclusive()


"""
complement operation
	- inverting all the bits
"""
def demo_complement():
	print('demo complement operation')
	a = 10
	print(bin(a))
	print(bin(~a))

# demo_complement()


"""
and operation
	- out put is 1 if both input is 1
"""
def demo_and():
	print('demo & operation')
	a = 10
	b = 9
	print(bin(a))
	print(bin(b))
	print(bin(a & b))


# demo_and()


"""
right shift by n bits
	- equal to divice with 2^n
"""
def demo_right_shift():
	print('demo right shift')
	a = 10
	print(bin(a))
	print(bin(a >> 2))
	print(a>>2)

# demo_right_shift()


def _rotr(x, y):
	# return ((x >> y) | (x << (32-y))) & 0xFFFFFFFF
	# print(bin(((x >> y) | (x << (32-y)))))
	print('{0:32b}'.format(x))
	print('{0:32b}'.format(x>>y))
	print('{0:32b}'.format(x<<(32-y)))
	print('{0:32b}'.format(((x >> y) | (x << (32-y)))))
	# print(bin(0xFFFFFFFF))
	# print('{0:32b}'.format(0xFFFFFFFF))


def demo_right_rotate_8bits_length(number, rotate_bits):


	# this function demo how to do right rotate with bit length is 8
	
	# print original number in binary format
	print('{0:8b}'.format(number))

	# make second part of original at right position by shift left (8-rotate_bits)
	after_left_shift = number << (8-rotate_bits)
	print('{0:8b}'.format(after_left_shift))

	# remove away first part of original number
	after_left_shift = after_left_shift & 0XFF
	print('{0:8b}'.format(after_left_shift))

	# make first part of original number at right position by shift right rotate_bits
	after_right_shift = number >> rotate_bits 
	print('{0:8b}'.format(after_right_shift))

	# do | operation to combine 2 result
	combine = after_left_shift | after_right_shift
	print('{0:8b}'.format(combine))

demo_right_rotate_8bits_length(9,2)





