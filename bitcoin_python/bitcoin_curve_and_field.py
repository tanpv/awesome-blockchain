"""
	Define a finite field for bitcoin base on FiniteField class
	Define a elliptic curve for bitcoin base on Point class
"""

from finite_field import FieldElement
from elliptic_curve import Point


# prime field applied for bitcoin
P = 2**256 - 2**32 -977

class S256Field(FieldElement):
	
	def __init__(self, num, prime=None):
		super().__init__(num=num, prime=P)

	# represent field element in hex
	def hex(self):
		return '{:x}'.format(self.num).zfill(64)

	def __repr__(self):
		return self.hex()


# elliptic curve parameter for bitcoin
A = 0
B = 7
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class S256Point(Point):

	bits = 256


	def __init__(self, x, y, a=None, b=None):	
		a, b = S256Field(A), S256Field(B)

		if x is None:
			super().__init__(x=None, y=None, a=a, b=b)
		elif type(x) == int:
			super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
		else:
			super().__init__(x=x, y=y, a=a, b=b)

	def __repr__(self):
		if self.x is None:
			return 'Point(infinity)'
		else:
			return 'Point({0},{1})'.format(self.x, self.y)



	# new way to doing scalar multiplication with faster result
	def __rmul__(self, coefficient):
		
		coef = coefficient % N
		current = self
		result = S256Point(None, None)

		for i in range(self.bits):
			# collect result when coef odd
			if coef & 1:
				result = result + current

			# multiple with 2 when coef even
			current = current + current

			# reduce coef to 2 by shift operation
			coef >>= 1

		return result


	# verify if signiture for message z is valid for a publish key
	def verify(self, z, sig):
		# 1/s = pow(s, N-2, N)
		s_inv = pow(sig.s, N-2, N)
		# u = z/s
		u = z * s_inv % N
		# v = r / s
		v = sig.r * s_inv % N
		# u*G + v*P
		total = u*G + v*self
		return total.x.num == sig.r




















