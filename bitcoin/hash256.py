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

import struct
import codecs
import hashlib
import sys
import copy


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


# demo_right_rotate_8bits_length(9,2)


"""
modulo by 2**32
https://stackoverflow.com/questions/11076216/re-implement-modulo-using-bit-shifts
"""
def demo_modulo_2_exponent_32(x):
	# x % 2**32 = x & (2**31 - 1)
	# 2**31 - 1 = 0xFFFFFFFF
	return x & 0xFFFFFFFF



class sha256():

	# 6 compress function used for hash 256

	def _ch(self,x,y,z):
		return (x & y) ^ ((~x) & z)

	def _maj(self,x,y,z):
		return (x & y) ^ (x & z) ^ (y & z)

	def _rotr(self,x,y):
		return (( x << (32-y)) & 0xFFFFFFFF | ( x>> y ))

	def _s0(self,x):
		return self._rotr(x,2) ^ self._rotr(x,13) ^ self._rotr(x,22)

	def _s1(self,x):
		return self._rotr(x,6) ^ self._rotr(x,11) ^ self._rotr(x,25)

	def _e0(self,x):
		return self._rotr(x,7) ^ self._rotr(x,18) ^ (x>>3) 
 
	def _e1(self,x):
		return self._rotr(x,17) ^ self._rotr(x,19) ^ (x>>10)


	# constants used for hash 256

	_k = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
		  0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
		  0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
		  0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
		  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
		  0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
		  0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
		  0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
		  0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)

	# init hash result
	_h = (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
		  0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19)

	_output_size = 8

	# init class with message
	def __init__(self, m=None):
		
		self._buffer = ''
		self._counter = 0

		# if m is not None:
		# 	if type(m) is not str:
		# 		raise 'Message should be string'
		self.update(m)

	
	def _hash256_one_block(self, one_block):

		# expanded message blocks
		w = [0]*64
		w[0:16] = struct.unpack('!16L', one_block)
		# # w[0:16] = one_block[0:16]
		# for i in range(0,16):
		# 	w[i] = one_block[i*4:i*4+4]

		print(w)

		for i in range(16,64):
			w[i] = (self._e0(w[i-15]) + w[i-7] + self._e1(w[i-2]) + w[i-16]) & 0xFFFFFFFF
		print(w)

		# init hash
		a,b,c,d,e,f,g,h = self._h

		for i in range(64):
			# calculate t1, t2
			t2 = (self._s0(a) + self._maj(a,b,c)) & 0xFFFFFFFF
			t1 = (h + self._s1(e) + self._ch(e,f,g) + self._k[i] + w[i]) & 0xFFFFFFFF

			# reassign
			h = g
			g = f
			f = e
			e = (d + t1) & 0xFFFFFFFF
			d = c
			c = b
			b = a
			a = (t1 + t2) & 0xFFFFFFFF

		# return hash
		self._h = [(x+y) & 0xFFFFFFFF for x,y in zip(self._h,[a,b,c,d,e,f,g,h])]

		return codecs.encode(b''.join([struct.pack('!L', i) for i in self._h[:self._output_size]]), 'hex_codec')
		# return b''.join([struct.pack('!L', i) for i in self._h[:self._output_size]])


	

	def update(self, m):
			# if not m:
			# 	return
			# if type(m) is not str:
			# 	raise 'Error'
			
			self._buffer += m
			self._counter += len(m)
			
			while len(self._buffer) >= 64:
				self._hash256_one_block(self._buffer[:64])
				self._buffer = self._buffer[64:]

	def digest(self):
		mdi = self._counter & 0x3F
		length = struct.pack('!Q', self._counter<<3)
		
		if mdi < 56:
			padlen = 55-mdi
		else:
			padlen = 119-mdi
		
		r = self.copy()
		a = b'\x80'.decode(errors="ignore")
		b = '\x00'*padlen
		c = b(length).decode(errors="ignore")

		d = a+b+c
		# c = b(b).decode(errors="ignore")
		r.update(b'\x80'.encode('utf-8') + length)
		return ''.join([struct.pack('!L', i) for i in r._h[:self._output_size]])

	def hexdigest(self):
		return self.digest().encode('hex')
		
	def copy(self):
		return copy.deepcopy(self)



print(sha256('abc').hexdigest())


h = hashlib.sha256()
h.update(b"abc")
print(h.hexdigest())


# print(len(one_block.encode('utf-8')))


# print('{0:32b}'.format(14))
# print('{0:32b}'.format(sha256()._rotr(14,15)))
# print([0]*64)
# 1234567890123456789012345678901234567890123456789012345678901234
# abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl




