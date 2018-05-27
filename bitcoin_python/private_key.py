"""
	- hold the secret key, is a random number
	- following method is implemented:
		- hex 	: represent private key as hexa number, with length 64 hex character
		- sign 	: create signature for message z, return signature
		- wif 	: convert private key to WIF format - follow process of 7 steps 
"""

import unittest
from unittest import TestCase


class PrivateKey:

	# hold secret
	# create public key by multiple generation point with secret
	def __init__(self, secret):
		self.secret = secret
		self.point = secret*G

	def hex(self):
		return '{:x}'.format(self.secret).zfill(64)

	def sign(self, z):
		pass


