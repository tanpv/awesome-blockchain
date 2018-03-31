"""
A minimum blockchain
	- understand how blocks are chain together
	- understand proof of work
"""

import time
import json
import hashlib


class Block(object):
	
	"""
		a block	contain following information
			- index
			- timestamp
			- data : this will be transaction in case of currency
			- proof : proof of work
			- previous_hash : hash string of previous block
	"""

	def __init__(self, index, timestamp, data,proof, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.proof = proof
		self.previous_hash = previous_hash



class BlockChain():

	"""
		a block chain manage following information
			- a chain of block
			- it's current transaction
	"""

	def __init__(self):
		# init a chain
		self.chain = []

		# define genesis_block
		genesis_block = Block(0, time.time(), 'this is first block', 0, '0')

		# search proof for first block
		self.search_proof_of_work(genesis_block)

		# add genesis block to chain
		self.add_block_to_chain(genesis_block)


	def hash_block(self, block):
		
		# using json to convert from object to json string
		block_string = 	str(block.index) + \
						str(block.timestamp) + \
						str(block.data) + \
						str(block.previous_hash) + \
						str(block.proof)

		# using hashlib to calculate sha256 of input json string
		return hashlib.sha256(block_string).hexdigest()

	
	def add_block_to_chain(self, block):
		self.chain.append(block)


	def get_last_block(self):
		return self.chain[-1]


	def search_proof_of_work(self,block):

		difficulty = '0000'

		# block string without proof
		block_string = 	str(block.index) + \
						str(block.timestamp) + \
						str(block.data) + \
						str(block.previous_hash)

		proof = 0

		while 1 :
			block_string_with_proof = block_string + str(proof)
			block_hash = hashlib.sha256(block_string_with_proof).hexdigest()
			if block_hash[:4] == difficulty:
				break
			proof = proof + 1

		block.proof = proof

		return block



new_chain = BlockChain()

block_num = 5

# previous_hash = new_chain.hash_block(new_chain.get_last_block())
# print previous_hash

for index in range(1, block_num+1):
	previous_hash = new_chain.hash_block(new_chain.get_last_block())
	# print previous_hash
	new_block = Block(index, time.time(), 'this is block {0}'.format(index), 0, previous_hash)
	new_block = new_chain.search_proof_of_work(new_block)
	new_chain.add_block_to_chain(new_block)


for block in new_chain.chain:
	print 'block'
	print json.dumps(block.__dict__, indent=4, sort_keys=False)
	print 'block_hash'
	print new_chain.hash_block(block)
	print '\n\n'
	time.sleep(1)






