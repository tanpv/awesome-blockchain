"""

A minimum blockchain

	- understand how blocks are chain together
	- understand proof of work
	- understand transaction and block creation
	- understand blockchain as service --- implement transaction and mining

"""


import time
import json
import hashlib
import requests
from flask import Flask, jsonify, request
from flask import Flask
from flask.json import JSONEncoder


class Block(object):
	
	"""
		a block	contain following information
			- index
			- timestamp
			- transaction : this will be transaction in case of currency
			- proof : proof of work
			- previous_hash : hash string of previous block
	"""

	def __init__(self, index, timestamp, transaction,proof, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.transaction = transaction
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
		self.current_transaction = []

		# define genesis_block
		genesis_block = Block(1, time.time(), 'this is first block', 0, '0')

		# search proof for first block
		self.search_proof_of_work(genesis_block)

		# add genesis block to chain
		self.chain.append(genesis_block)


	def hash_block(self, block):
		
		# using json to convert from object to json string
		block_string = 	str(block.index) + \
						str(block.timestamp) + \
						str(block.transaction) + \
						str(block.previous_hash) + \
						str(block.proof)

		# using hashlib to calculate sha256 of input json string
		return hashlib.sha256(block_string).hexdigest()

	
	def add_block_to_chain(self):
		
		index = len(self.chain) + 1
		timestamp = time.time()
		transaction = self.current_transaction
		previous_hash = self.hash_block(self.chain[-1])
		proof = '0'

		new_block = Block(index, timestamp, transaction, proof, previous_hash)

		new_block = self.search_proof_of_work(new_block)

		self.chain.append(new_block)

		self.current_transaction = []

		return new_block


	def get_last_block(self):
		return self.chain[-1]



	def search_proof_of_work(self,block):

		difficulty = '0000'

		# block string without proof
		block_string = 	str(block.index) + \
						str(block.timestamp) + \
						str(block.transaction) + \
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


	def new_transaction(self, sender, recipient, amount):

		"""
			- append to transaction
			- return the block which will added transaction to
		"""
		self.current_transaction.append({
			'sender': sender,
			'recipient' : recipient,
			'amount' : amount,
			})

		return len(self.chain)

	def serialize(self):
		return {
			'index': self.index,
			'timestamp': self.timestamp,
			'transaction': self.transaction,
			'proof': self.proof,
			'previous_hash':self.previous_hash,
		}


############################### blockchain as service ####################


app = Flask(__name__)
app.json_encoder = JSONEncoder
 

# init new chain
new_chain = BlockChain()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	required = ['sender', 'recipient', 'amount']

	# Create a new transaction
	index = new_chain.new_transaction(values['sender'], values['recipient'], values['amount'])

	response = {'message': 'transaction will be added to block {0}'.format(index)}

	return jsonify(response)



@app.route('/chain', methods=['GET'])
def chain():

	response = {
		'chain': [b.__dict__ for b in new_chain.chain],
		'length': len(new_chain.chain)
	}

	return jsonify(response), 200




@app.route('/mine', methods=['GET'])
def mine():

	new_block = new_chain.add_block_to_chain()
	
	new_chain.new_transaction(sender='0', recipient='', amount=1,)
	
	response = {
		'message': 'new block added',
		'index': new_block.index,
		'transaction': new_block.transaction,
		'proof': new_block.proof,
		'previous_hash': new_block.previous_hash,
	}

	return jsonify(response), 200


if __name__ == "__main__":
	app.run()

