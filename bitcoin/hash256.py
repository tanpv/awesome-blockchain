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

demo_exclusive()


"""
complement operation
	- inverting all the bits
"""
def demo_complement():
	print('demo complement operation')
	a = 10
	print(bin(a))
	print(bin(~a))

demo_complement()


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


demo_and()


"""
right shift by n bits
	- equal to multiply with 2^n
"""
def demo_right_shift():
	print('demo right shift')
	a = 10
	print(bin(a))
	print(bin(a << 2))
	print(a<<2)

demo_right_shift()


"""
right rotation by n bits
	how to calculate rotation
	https://www.youtube.com/watch?v=S2yXCBu3NdQ
"""



