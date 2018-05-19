"""
	- define a class which represent point on elliptic curve and all
	operation happend on that curve

	- a elliptic curve is defined by two parameter a and b
	y**2 = x**3 + x*a + b

	- a point on elliptic curve is defined by a, b and 2 cordinate x, y
	
	- following operation are defined on elliptic curve
		- compare equal
		- compare not equal
		- add point to point
		- scalar multiplication with point
"""

from unittest import TestCase
import unittest

class Point():

	def __init__(self, x, y, a, b):
	
		self.a = a
		self.b = b
		self.x = x
		self.y = y

		if self.x is None and self.y is None:
			return

		# check if the point is on curve
		if self.y**2 != self.x**3 + self.a*self.x + self.b:
			raise RuntimeError('Point({0},{1}) is not on curve where a,b = {2},{3}'.format(x,y,a,b))

	# if 2 point on curve is same
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

	def __ne__(self, other):
		# check if on same curve
		if self.a != other.a or self.b != other.b:
			raise RuntimeError('could not compare two points on difference curve')

		return self.x != other.x or self.y != other.y

	def __repr__(self):
		if self.x is None:
			return 'Point(ifinity)'
		else:
			return 'Point({0},{1})'.format(self.x, self.y)

	def __add__(self, other):
		# check if on the same curve
		if self.a != other.a or self.b != other.b:
			raise RuntimeError('could not add point on difference curve')

		# if one of two number is ifinity
		if self.x is None:
			return other
		if other.x is None:
			return self

		# if two number have same x and diff y --> the sum is ifinity
		if self.x == other.x and self.y != other.y:
			return self.__class__(None, None, self.a, self.b)

		# add 2 point if x1 != x2
		if self.x != other.x:
			# use viet theorem
			# calculate slope
			s = (self.y - other.y) / (self.x - other.x)
			# x3 = s**2 - x1 - x2
			x = s**2 - self.x - other.x
			# y3 = -(s*(x3-x1) + y1)
			# y3 = s*(x1-x3) - y1
			y = s*(self.x - x) - self.y
			return self.__class__(x,y,self.a,self.b)
		else:
			# add one point to it self
			# y**2 = x**3 + ax + b
			# 2ydy = 3x**2dx + a
			# slop = dy/dx = (3x**2 + a) / 2y
			s = (3*self.x**2+self.a) / (2*self.y)
			x = s**2 - 2*self.x
			y = s*(self.x - x) - self.y
			return self.__class__(x,y,self.a,self.b)

	def __rmul__(self, coefficcient):
		# use add operaton to do scalar multiple
		product = self.__class__(None, None, self.a, self.b)
		for _ in range(coefficcient):
			product += self

		return product



# eliptic curve test over field of real number 
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


		










