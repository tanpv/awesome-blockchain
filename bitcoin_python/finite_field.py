"""
Create a class which control field element
	- a element is defined by it value and prime number
	which is order of field

	- define following operation for the field
		- compare equal
		- compare not equal
		- present of class
		- following module operation is defined
			- add
			- sub
			- multiple
			- power
			- division

"""


from unittest import TestCase
import unittest



class FieldElement():
	def __init__(self, num, prime):
		# check if field element is valid
		if num < 0 or num > prime:
			raise ValueError('num should between 0 and {0}-1'.format(prime))

		self.num = num
		self.prime = prime

	def __eq__(self, other):
		# equal when same prime order and number
		return self.num == other.num and self.prime == other.prime			

	def __ne__(self, other):
		return self.num != other.num or self.prime != other.prime

	def __repr__(self):
		return 'FieldElement_{}({})'.format(self.prime, self.num)

	def __add__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('could not add 2 number in different fields')

		num = (self.num + other.num) % self.prime
		# return a instant of this class
		return self.__class__(num, self.prime)

	def __sub__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('could not sub 2 nuber in different fields')
		
		num = (self.num - other.num) % self.prime
		return self.__class__(num, self.prime)

	def __mul__(self,other):
		if self.prime != other.prime:
			raise ValueError('could not multiple 2 number in different fields')

		num = (self.num * other.num) % self.prime
		return self.__class__(num, self.prime)

	# multiple a field element with a number
	def __rmul__(self, coefficient):
		num = (self.num*coefficient) % self.prime
		return self.__class__(num, self.prime)

	def __pow__(self, n):
		"""
		fermat little theorem : num**(p-1) % p = 1
		calculate    : num**n % p
		= num**(a(p-1)+b)
		= num**(a(p-1)) * num**b with b = n % p-1
		= 1 * num**b %p because (num**a)**(p-1) % p = 1 with p is prime
		= num**b % p with b = n%p-1

		reduce alot of effort caculation when n > p
		"""
		num = pow(self.num, n%(self.prime-1), self.prime)
		return self.__class__(num, self.prime)

	def __truediv__(self, other):
		if self.prime != other.prime:
			raise RuntimeError('can not divide two number in different fields')

		"""
			Use fermat little theorem\\
			a/b % p
			= a.(b**-1) % p
			= a.b**p-2 % p because b**p-1 % p = 1 
		"""
		num = (self.num * pow(other.num, self.prime-2, self.prime)) % self.prime
		return self.__class__(num, self.prime)



"""
	Test for FieldElement
"""
class  FieldElementTest(TestCase):

	def test_add(self):
		a = FieldElement(2,13)
		b = FieldElement(3,13)
		self.assertEqual(a+b,FieldElement(5,13))

	def test_sub(self):
		a = FieldElement(3,13)
		b = FieldElement(2,13)
		self.assertEqual(a-b, FieldElement(1,13))

	def test_mul(self):
		a = FieldElement(2,13)
		b = FieldElement(3,13)
		self.assertEqual(a*b,FieldElement(6,13))

	def test_pow(self):
		a = FieldElement(2,13)
		self.assertEqual(a**3, FieldElement(8,13))

	def test_div(self):
		a = FieldElement(6,13)
		b = FieldElement(2,13)
		self.assertEqual(a/b, FieldElement(3,13))


if __name__ == '__main__':
	unittest.main()












