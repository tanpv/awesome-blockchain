### Introduction and Installation

This tutorial intent to make clear about blockchain structure, and other important idea related to blockchain : proof of work, transaction, distributed client and consensus algorithm.

Please download and install Anaconda as python coding environment for this course. Please note to chose 3.6 version.

https://www.anaconda.com/download/



### Hash function

A hash function is a function that takes input and create output with following property:

* Input could be any length but out put is fixed length of string
* It is easy to compute output from input but it is impossible to compute input if know output
* 2 difference input will create 2 difference output hash string



Hash string of data like finger print of that data and present for that data, because any change in data will make hash string change in random fashion. 



![Rosenbaum_CHaB_05](C:\out\blockchain_code\blockchain\Rosenbaum_CHaB_05.png)



Now, let see how we compute hash with python.

```python
# hashlib is standard python lib use for calculate hash string
import hashlib

# from now on we will use hash function sha256, this hash is used in bitcoin
# and many other crypto currency
print('sha256 for "Hello!" string')
print(hashlib.sha256(b'Hello!').hexdigest())

# a small of input make completely random difference in output
print('sha256 for "Hello" string')
print(hashlib.sha256(b'Hello').hexdigest())
```

Running above code you will see that out put of sha256 is string of 64 hex character, so it correspond of length of 256 bits. Out put of sha256 hash function is 256 bits. 



### Blockchain

At it core, blockchain structure is fairly simple. It contain blocks and blocks are chained together, **"chained together"** basically meant the higher block contain hash string of block right below it. Please see the image below.

![blockchain](C:\out\blockchain_code\blockchain\blockchain.jpg)



Now let's create Block class to model a block

```python
class Block(object):
	
	"""
		a block	contain following information
			- index : the order which block is added to chain
			- timestamp : moment which block is added to chain
			- data : this will be transaction in case of currency
			- previous_hash : hash string of previous block
	"""

	def __init__(self, 
				index, 
				timestamp, 
				data, 
				previous_hash):

		self.index = index
		self.timestamp = timestamp
		self.data = data
		self.previous_hash = previous_hash
```



A blockchain will contain a chain which store all it's blocks, and some methods like : hash_block, add_block_to_chain, get_last_block. Following code demo a blockchain.

```python
class BlockChain():

	"""
		a block chain manage following information
			- a chain of block
	"""

	def __init__(self):
		# init a chain
		self.chain = []

		# define genesis_block
		genesis_block = Block(0, time.time(), 'this is first block', '0')

		# add genesis block to chain
		self.add_block_to_chain(genesis_block)


	def hash_block(self, block):
		
		# using json to convert from object to json string
		block_string = json.dumps(block.__dict__)

		# using hashlib to calculate sha256 of input json string
		return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

	
	def add_block_to_chain(self, block):
		self.chain.append(block)


	def get_last_block(self):
		return self.chain[-1]
```



Now, create one chain, add some block then read it again to actually see how the block chained together.

```python
# create a new chain
new_chain = BlockChain()


# add some blocks to chain
block_num = 5
for index in range(1, block_num+1):
	previous_hash = new_chain.hash_block(new_chain.get_last_block())
	# print previous_hash
	time.sleep(0.2)
	new_block = Block(index, time.time(), 'this is block {0}'.format(index), previous_hash)
	new_chain.add_block_to_chain(new_block)



# read out the chain after added block
for block in new_chain.chain:
	print('block')
	print(json.dumps(block.__dict__, indent=4, sort_keys=False))
	print('sha256 of block')
	print(new_chain.hash_block(block))
	print('\n\n')
```



Following result will show up from console log, this is valid chain due to block is chained together by sha256 hash function. Until now the link between blocks should be absolute clear!.

![2018-04-08_20-45-15](C:\out\blockchain_code\blockchain\2018-04-08_20-45-15.png)



### Proof of work, mining and mining difficulty

#### Why need proof of work ?

In blockchain like bitcoin, proof of work is essential on consensus algorithm which is algorithm to decide which transaction is valid and could be added to the chain.

#### What is proof of work ?

Let start with following simple block data which is present as a python dictionary type.

```python
block = {

    'index': 1,

    'timestamp': 1506057125.900785,

    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],	
    
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```

Let create hash for above block

```python
# normal sha256 calculation
print(hashlib.sha256(json.dumps(block).encode('utf-8')).hexdigest())
```

We will get result is a long string like this

```python
f8b91672ff39ec64e294929dd1bbd7fbe7c21da6174c79e9819ffb0ef13aa08c
```

Now let setting up a problem like this, find a value (>= 0) for variable name `proof` which hash combination of block and `proof` will start with character '0'. Because we do not know which kind of input value for `proof` will create hash string start with character '0', so we do brute force for every value of `proof`.

Let do the code to find out `proof`

```python
import hashlib
import json

block = {

    'index': 1,

    'timestamp': 1506057125.900785,

    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],

    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}


def isvalidproof(proof):
    
    block_string = json.dumps(block)

    hash_with_proof = hashlib.sha256(str(proof).encode('utf-8') + block_string.encode('utf-8')).hexdigest()    
    
    print(hash_with_proof)

    # difficulty '0000' is easy
    # difficulty '00000' is extream hard
    if hash_with_proof[:1] == '0':
    
        return 0
    
    else:
    
        return 1

proof = 0

while isvalidproof(proof):
    proof = proof + 1

print(proof)
```



Running this code, we find out that hash string will start with 1 0 number '0xxx' with `proof` = 32. This value of `proof` variable is called `proof of work` just because of we already do some calculation work in order to find out right value for `proof` 

Let's do another interesting thing, what if we increase the requirement like : find `proof` so the hash string start with 2 number 0 '00xxx'. Let change the code and try to run. This time we found `proof` = 40. Then if we require hash start with 3 number 0 '000xxx' we will found `proof` = 1898 (mean go to loop 1898 times).

So it is harder to find `proof` when we increase the number of 0 which hash string need to start with. The number 0 which has string need to start with is called `difficulty` of `proof of work` algorithm.

Please note that which only requirement of hash string start with 5 number 0 '00000xxx', it take my Dell laptop to run forever but not yet found right value for `proof` 

The action of calculate hash string which solve above problem is call `mining` .



#### Blockchain with proof of work



Let put the idea about `proof of work` to blockchain. Because of `proof of work` blockchain like Bitcoin become really secure.

One variable called `proof` is added to Block class.

```python
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
```



Now then add function call `search_proof_of_work`

```python
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
		block_hash = hashlib.sha256(block_string_with_proof.encode('utf-8')).hexdigest()
		if block_hash[:4] == difficulty:
			break
		proof = proof + 1

	block.proof = proof

	return block
```

 

Running the code and we have blockchain is printed with right value of proof.

![2018-04-12_22-03-24](C:\out\blockchain_code\blockchain\2018-04-12_22-03-24.png)



### Transaction and block creation

The most important part of blockchain is it's data, in this course that will be transaction data between sender and recipient like bitcoin or other crypto currency.

Let's adding one more variable to blockchain class called `current_transaction` , this variable will manage the transaction which happen.

A transaction will contain following input : `sender` , `recipient` , `amount`  

Now let's do the code

```python
def __init__(self):
		# init a chain
		self.chain = []
         # init transaction list
		self.current_transaction = []
        
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
```

Let try to run the code and we will see transaction data inside blockchain.

![2018-04-12_22-42-28](C:\out\blockchain_code\blockchain\2018-04-12_22-42-28.png)



### Blockchain as a service

In real, blockchain is running on a distributed system which contain multiple node. In this session we will try to use flask and REST api to make each node become server which could serve request.

```python
from flask import Flask
app = Flask(__name__)
app.json_encoder = JSONEncoder
 

# init new chain
new_chain = BlockChain()

@app.route("/mine", methods=['GET'])
def mine():
	return "start mine"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	return "start transaction"

@app.route('/chain', methods=['GET'])
def chain():
	return "the chain"
	
if __name__ == "__main__":
	app.run()

```



### Transaction and mining service

Now let's really building transaction and mining service.

```python
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

```



### Consensus algorithm

In the world of consensus between multiple node, the longest node win.



