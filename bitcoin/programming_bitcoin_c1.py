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


if __name__ == '__main__':
	unittest.main()


