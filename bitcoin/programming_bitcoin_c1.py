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


	def __pow__(self, other):
		if self.prime != other.prim:
			raise RuntimeError('can not pow two number in different fields')
		num = (self.num ** other.num) % self.prime
		return self.__class__(num, self.prime)



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











a = FieldElement(3, 13)
b = FieldElement(12, 13)
c = FieldElement(10, 13)

print(a*b==c)

l = [1, 3, 7, 13, 18]

for k in range(1000):
	print([item%19 for item in l])








