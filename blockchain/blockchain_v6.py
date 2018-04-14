"""
	A minimum blockchain
	- understand how blocks are chain together
	- understand proof of work
	- understand transaction and block creation
	- understand blockchain as service --- implement transaction and mining
	- understand blockchain consensus
"""


import time
import json
import hashlib
import requests
from flask import Flask, jsonify, request
from flask import Flask
from flask.json import JSONEncoder
from uuid import uuid4
from urllib.parse import urlparse
from collections import namedtuple

class Block():
    
    """
        a block    contain following information
            - index
            - timestamp
            - transaction : this will be transaction in case of currency
            - proof : proof of work
            - previous_hash : hash string of previous block
    """

    def __init__(self,
                 index, 
                 timestamp, 
                 transaction,
                 proof, 
                 previous_hash):

        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.proof = proof
    


class BlockChain():

    """
        a block chain manage following information
            - a chain of block
            - it's current transaction
    """

    def __init__(self):
        # manage blockchain, store blocks
        self.chain = []
        # manage transaction, store transaction
        self.current_transaction = []
        # manage node, store node
        self.nodes = set()


        # define genesis_block
        genesis_block = Block(1, time.time(), 'this is first block', 0, '0')

        # search proof for first block
        self.search_proof_of_work(genesis_block)

        # add genesis block to chain
        self.chain.append(genesis_block)



    def hash_block(self, block):
        
        # using json to convert from object to json string
        block_string =     str(block.index) + \
                        str(block.timestamp) + \
                        str(block.transaction) + \
                        str(block.previous_hash) + \
                        str(block.proof)

        # using hashlib to calculate sha256 of input json string
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


    
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
        block_string =     str(block.index) + \
                        str(block.timestamp) + \
                        str(block.transaction) + \
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




    def valide_chain(self, chain):

        """
            - check if 2 block is continous, hash of below block should equal 
            to hash property of above block.
            
            - check if proof of work found for each block is correct. 

        """

        index = 1
        below_block = chain[0]

        while index < len(chain):
            
            above_block = chain[index]
            
            print(json.dumps(below_block.__dict__))
            print(self.hash_block(below_block))
            print(json.dumps(above_block.__dict__))

            # check if block chain together and hash is calculate correctly
            if above_block.previous_hash != self.hash_block(below_block):
                # print(index)
                # print(above_block.previous_hash)
                # print(self.hash_block(below_block))
                print('fail because diff hash')
                return False

            # check if pow is correct on each hash
            below_block_hash = self.hash_block(below_block)
            if below_block_hash[:4] != '0000':
                print('fail because proof of work')
                return False

            # check on next block
            below_block = above_block
            index = index + 1

        print('true')
        return True


    

    def register_node(self, address):
        """
            parse 
        """
        url = urlparse(address)
        if url.netloc:
            self.nodes.add(url.netloc)


    def resolve_conflicts(self):
        
        """
            consensus algorithm, resolves conflicts by replacing
            local chain with longest chain
        """

        neighbours = self.nodes
        new_chain = None

        # init max length
        max_length = len(self.chain)

        # check for all lable
        for node in neighbours:
            response = requests.get('http://{0}/chain'.format(node))

            if response.status_code == 200:
                
                length = response.json()['length']
                chain = response.json()['chain']
                print(length)
                print(max_length)
                print(chain)

                neighbour_chain = []

                for block in chain:
                    print(block)
                    block_dict = json.loads(str(block))
                    new_block = Block(block_dict['index'],
                                    block_dict['timestamp'],
                                    block_dict['transaction'],
                                    block_dict['proof'],
                                    block_dict['previous_hash'])
                    neighbour_chain.append(new_block)

                    # def __init__(self,
                    #                  index, 
                    #                  timestamp, 
                    #                  transaction,
                    #                  proof, 
                    #                  previous_hash):


                if length > max_length and self.valide_chain(neighbour_chain):
                    max_length = length
                    new_chain = neighbour_chain

        # Replace our chain with discovered new chain
        if new_chain:
            self.chain = new_chain
            return  True

        return  False



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

node_identifier = str(uuid4()).replace('-','')

# init new chain
new_chain = BlockChain()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    # if not all(k in values for k in required):
    #     return 'Missing values', 400

    # Create a new transaction
    index = new_chain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'transaction will be added to block {0}'.format(index)}

    return jsonify(response)



@app.route('/chain', methods=['GET'])
def chain():

    response = {
        'chain': [json.dumps(b.__dict__) for b in new_chain.chain],
        'length': len(new_chain.chain)
    }

    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():

    # sender = 0 mean this coin is created from mining process
    new_chain.new_transaction(sender='0', recipient='', amount=1,)
    # add block to chain
    new_block = new_chain.add_block_to_chain()
    
    
    
    response = {
        'message': 'new block added',
        'index': new_block.index,
        'transaction': new_block.transaction,
        'proof': new_block.proof,
        'previous_hash': new_block.previous_hash,
    }

    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()

    print(values)

    nodes = values.get('nodes')


    for node in nodes:
        new_chain.register_node(node)

    response = {
        'message' : 'New nodes have been added',
        'total_nodes' : list(new_chain.nodes),
    }

    return jsonify(response), 201



@app.route('/nodes/resolve', methods=['GET'])
def consensus():

    replaced = new_chain.resolve_conflicts()

    if replaced:

        response = {
            'message': 'our chain was replaced',
            'new_chain': [json.dumps(b.__dict__) for b in new_chain.chain]
        }

    else:
        
        response = {
            'message': 'our chain is authoritative',
            'chain': [json.dumps(b.__dict__) for b in new_chain.chain],
        }

    return jsonify(response), 200


@app.route('/valide', methods=['GET'])
def valide():
    result = new_chain.valide_chain(new_chain.chain)
    response = {
        'result':result,
    }
    return jsonify(response), 200


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5000,type=int,help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)

