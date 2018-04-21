from unittest import TestCase
import unittest

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
			raise RuntimeError('can not multiple two number in different fields')
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

		# check if point on the curve
		if self.y**2 != self.x**3 + self.a*self.x + self.b:
			raise ValueError('Point ({},{}) is not on the curve where a,b={},{}'.format(x,y,a,b))

	def __eq__(self, other):
		# same curve and same cordinate
		return self.a == other.a and self.b == other.b and self.x == other.x and self.y == other.y

	def __ne__(self, other):
		if self.a != other.a or self.b != other.b:
			raise RuntimeError('could not compare 2 points which not in same curve')

		return self.x != other.x or self.y != other.y


if __name__ == '__main__':
	unittest.main()



