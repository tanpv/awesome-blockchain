### Introduction and Installation

This tutorial intent to make clear about blockchain structure, and other important idea related to blockchain : proof of work, transaction, distributed client and consensus algorithm.

Please download and install Anaconda as python coding environment for this course

https://www.anaconda.com/download/



### Hashing

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

Let start with following simple block data which is present as a JSON object.

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

    'proof': 0,

    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```

Compare with block structure on blockchain session, we could see that have one more field called "proof".

Let create 





### Transaction and block creation

### Blockchain as a service

### Transaction and mining service

### Consensus algorithm
