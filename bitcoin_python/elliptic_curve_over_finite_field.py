"""
	This is test operation of elliptic curve over finite field.
	
	You will see that all elliptic curve operation still 
	same as on real number field
"""


import unittest

from finite_field import FieldElement
from elliptic_curve import Point
from unittest import TestCase


class  EECtest(TestCase):

	def test_point_on_curve(self):

		# define number in prime finite field
		prime = 223
		a = FieldElement(0, prime)
		b = FieldElement(7, prime)

		# define some valid and invalid poin
		valid_points = ((192,105), (17,56), (1,193))
		invalid_points = ((200,119),(42,99))

		# check if these point are valid on elliptic curve
		for x_raw, y_raw in valid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)
			# create a valid point on curve
			Point(x,y,a,b)

		# check if these point are invalid on elliptic curve
		for x_raw, y_raw in invalid_points:
			x = FieldElement(x_raw, prime)
			y = FieldElement(y_raw, prime)
			with self.assertRaises(RuntimeError):
				Point(x,y,a,b)


	def test_add(self):
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



if __name__ == '__main__':
	unittest.main()