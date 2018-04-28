from unittest import TestCase
import unittest
import hashlib

def hash160(message):
	return hashlib.new('ripemd160', hashlib.sha256(message).digest()).digest()

def double_sha256(message):
	return hashlib.sha256(hashlib.sha256(message).digest()).digest()


"""
	Define a finite field element
"""

class FieldElement:

	def __init__(self, num, prime):
		if num < 0 or num >= prime:
			raise ValueError('num should be between 0 and {}-1'.format(prime))

		self.num = num
		self.prime = prime

	def  __eq__(self, other):
		return self.num == other.num and self.prime == other.prime

	def __ne__(self, other):
		if other is None:
			return True
		return self.num != other.num or self.prime != other.prime

	def __repr__(self):
		return 'FieldElement_{}({})'.format(self.prime, self.num)		

	def __add__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('can not add two numbers in different fields')
		num = (self.num + other.num) % self.prime
		return self.__class__(num, self.prime)


	def __sub__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('can not sub two number in different fields')
		num = (self.num - other.num) % self.prime
		return self.__class__(num, self.prime)


	def __mul__(self, other):
		if self.prime != other.prime:
			raise ValueError('can not multiple two number in different fields')
		num = (self.num * other.num) % self.prime
		return self.__class__(num, self.prime)


	# def __pow__(self, n):
	# 	num = (self.num ** n) % self.prime
	# 	return self.__class__(num, self.prime)

	# better version of __pow__ function
	# use fermat's little theorem
	# decrease n to n%prime
	def __pow__(self, n):
		num = pow(self.num, n % self.prime, self.prime)
		return self.__class__(num, self.prime)

	# convert div to pow
	def __truediv__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('can not divide two nummber in different fields')

		# use fermat's little theorem
		num = (self.num * pow(other.num, self.prime-2, self.prime))%self.prime
		return self.__class__(num, self.prime)


# write testing for FieldElement
# test driven method
class FieldElementTest(TestCase):

	def test_add(self):
		a = FieldElement(2,31)
		b = FieldElement(15,31)
		self.assertEqual(a+b,FieldElement(17,31))
		a = FieldElement(19,31)
		b = FieldElement(20,31)
		self.assertEqual(a+b,FieldElement(8,31))

	def test_sub(self):
		a = FieldElement(29,31)
		b = FieldElement(4,31)
		self.assertEqual(a-b,FieldElement(25,31))
		a = FieldElement(15,31)
		b = FieldElement(30,31)
		self.assertEqual(a-b,FieldElement(16,31))

	def test_mul(self):
		a = FieldElement(24, 31)
		b = FieldElement(19, 31)
		self.assertEqual(a*b,FieldElement(22,31))

	def test_pow(self):
		a = FieldElement(17,31)
		self.assertEqual(a**3, FieldElement(15,31))

	def test_div(self):
		a = FieldElement(3,31)
		b = FieldElement(24,31)
		self.assertEqual(a/b, FieldElement(4,31))



class Point:

	def __init__(self, x, y, a, b):	
		self.a = a
		self.b = b
		self.x = x
		self.y = y

		if self.x is None and self.y is None:
			return

		# check if point on the curve
		if self.y**2 != self.x**3 + self.a*self.x + self.b:
			raise RuntimeError('Point ({},{}) is not on the curve where a,b={},{}'.format(x,y,a,b))

	def __eq__(self, other):
		# same curve and same cordinate
		return self.a == other.a and self.b == other.b and self.x == other.x and self.y == other.y

	def __ne__(self, other):
		if self.a != other.a or self.b != other.b:
			raise RuntimeError('could not compare 2 points which not in same curve')

		return self.x != other.x or self.y != other.y

	# print object as string
	def __repr__(self):
		if self.x is None:
			return 'Point(ifinity)'
		else:
			return 'Point({},{})'.format(self.x, self.y)

	# point addition
	def __add__(self, other):
		if self.a != other.a or self.b != other.b:
			raise RuntimeError('Could not do point addition in different curve')

		# one of 2 number is ifinity
		if self.x is None:
			return other
		if other.x is None:
			return self

		# if two number has same x, their sum should be ifinity
		if self.x == other.x and self.y != other.y:
			return self.__class__(None, None, self.a, self.b)

		# add 2 difference point
		if self.x != other.x:
			# calculate slope
			s = (self.y - other.y) / (self.x - other.x)
			# calculate x3 from s and x1, x2
			x = s**2 - self.x - other.x
			# calculate y3
			y = s*(self.x-x) - self.y
			return self.__class__(x,y,self.a,self.b)
		# add one point to it self --> apply to calculate multiple point with coefficient
		else:
			s = (3*self.x**2 + self.a) / (2*self.y)
			x = s**2 - 2*self.x
			y = s*(self.x-x) - self.y
			return self.__class__(x,y,self.a,self.b)


	# point scalar multiple
	def __rmul__(self, coefficient):
		product = self.__class__(None, None, self.a, self.b)
		for _ in range(coefficient):
			product += self
		return product


# test class for Point class
class PointTest(TestCase):

	def test_on_curve(self):
		with self.assertRaises(RuntimeError):
			Point(x=-2, y=4, a=5, b=7)

		Point(x=3, y=-7, a=5, b=7)
		Point(x=18, y=77, a=5, b=7)


	def test_add0(self):
		# define a ifinity point
		a = Point(x=None, y=None, a=5, b=7)
		b = Point(x=2, y=5, a=5, b=7)
		c = Point(x=2, y=-5, a=5, b=7)

		# sum of a point and ifinity
		self.assertEqual(a+b, b)
		self.assertEqual(b+a, b)

		# sum of 2 points 
		self.assertEqual(b+c, a)

	def test_add1(self):
		# add two difference normal point
		a = Point(x=3, y=7, a=5, b=7)
		b = Point(x=-1, y=-1, a=5, b=7)
		# c = Point(x=2, y=-5, a=5, b=7)

		self.assertEqual(a+b, Point(x=2, y=-5, a=5, b=7))
		
	def test_add2(self):
		# add one point to it self
		a = Point(x=-1,y=1,a=5,b=7)
		self.assertEqual(a+a, Point(x=18,y=-77,a=5,b=7))


# check eec on a finite field
class EECTest(TestCase):

	def test_on_curve(self):
		# define upper limit prime
		prime = 223
		# define a point in finite prime field
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)

		# define some valid and invalid poin
		valid_points = ((192,105), (17,56), (1,193))
		invalid_points = ((200,119),(42,99))

		# check over valid points
		for x_raw, y_raw in valid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)

			# a valid point on EEC is formed 
			Point(x, y, a, b)

		for x_raw, y_raw in invalid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)
			with self.assertRaises(RuntimeError):
				Point(x,y,a,b)


	def test_add1(self):
		# test add point on bitcoin curve over finite prime field
		prime = 223
		# define parameter for curve
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)

		additions = (
			# (x1, y1, x2, y2, x3, y3)		 
			(192, 105, 17, 56, 170, 142),
			(47, 71, 117, 141, 60, 139),
			(143, 98, 76, 66, 47, 71),
		)

		for x1_raw, y1_raw, x2_raw, y2_raw, x3_raw, y3_raw in additions:
			
			# define field then define on curve
			x1 = FieldElement(x1_raw, prime)
			y1 = FieldElement(y1_raw, prime)
			p1 = Point(x1, y1, a, b)

			x2 = FieldElement(x2_raw, prime)
			y2 = FieldElement(y2_raw, prime)
			p2 = Point(x2, y2, a, b)

			x3 = FieldElement(x3_raw, prime)
			y3 = FieldElement(y3_raw, prime)
			p3 = Point(x3, y3, a, b)

			self.assertEqual(p1+p2, p3)

	def test_rmul(self):
		
		prime = 223
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)

		multiplications = (
			# (coefficient, x1, y1, x2, y2)
			(2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
		)

		for s, x1_raw, y1_raw, x2_raw, y2_raw in multiplications:
			
			x1 = FieldElement(x1_raw, prime)
			y1 = FieldElement(y1_raw, prime)
			p1 = Point(x1, y1, a, b)

			if x2_raw is None:
				p2 = Point(None, None, a, b)
			else:
				x2 = FieldElement(x2_raw, prime)
				y2 = FieldElement(y2_raw, prime)
				p2 = Point(x2, y2, a, b)

			self.assertEqual(s*p1, p2)


# define bitcoin parameter
A = 0
B = 7
P = 2**256 - 2**32 -977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# drive from FieldElement
class  S256Field(FieldElement):
	
	def __init__(self, num, prime=None):
		super().__init__(num=num, prime=P)

	def hex(self):
		return '{:x}'.format(self.num).zfill(64)

	def __repr__(self):
		return self.hex()


class S256Point(Point):
	bits = 256

	def __init__(self, x, y, a=None, b=None):
		a, b = S256Field(A), S256Field(B)
		if x is None:
			supper().__init__(x=None, y=None, a=a, b=b)
		elif type(x) == int:
			super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
		else:
			super().__init__(x=x, y=y, a=a, b=b)

	def __repr__(self):
		if self.x is None:
			return 'Point(infinity)'
		else:
			return 'Point({},{})'.format(self.x, self.y)

	def __rmul__(self, coefficient):
		coef = coefficient % N
		current = self
		result = S256Point(None, None)

		for i in range(self.bits):
			
			# if coef is odd
			if coef & 1:
				result = result + current

			# multiple with 2
			current = current + current
			result = current

			# divide coef by 2 with shift operation
			coef >>= 1

		return result

	def sec(self, compressed=True):
		if compressed:
			if self.y.num % 2 == 0:
				return b'\x02' + self.x.num.to_bytes(32, 'big')
			else:
				return b'\x03' + self.x.num.to_bytes(32, 'big')
		else:
			return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')


	def address(self, compressed=True, testnet=False):
		# building address from publish key
		sec = self.sec(compressed)
		h160 = hash160(sec)

		if testnet:
			prefix = b'\x6f'
		else:
			prefix = b'\x00'

		raw = prefix + h160

		checksum = double_sha256(raw)[:4]


alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

# convert from int number to base 58 number
def encode_base58(num):
	# init the result
	encode = ''
	# number of character inside alphabet
	base_count = len(alphabet)
	# continue to convert if num still > base number
	while (num >= base_count):
		# get the div
		tmp = num // base_count
		print(tmp)
		# get the mod
		mod = num % base_count
		print(mod)
		# access character inside table
		encode = alphabet[int(mod)] + encode
		print(encode)
		# continue the loop
		num = tmp
		print('--------------')

	# final add if num != 0
	if (num):
		encode = alphabet[int(num)] + encode

	return encode


def decode_base58(num_str):
	decode = 0
	power = len(num_str)-1
	for c in num_str:

		print(alphabet.index(c))
		# print(c)
		decode = decode + alphabet.index(c)*(58**power)
		power  = power - 1
		print(decode)
	return decode


print(encode_base58(99999))
print(decode_base58('vJ8'))
print(decode_base58(encode_base58(888888)))












		







# if __name__ == '__main__':
# 	unittest.main()


