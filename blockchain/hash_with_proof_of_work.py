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

    'proof': 0,

    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}



def isvalidproof(proof):
    
    block_string = json.dumps(block)

    hash_with_proof = hashlib.sha256(str(proof).encode('utf-8') + block_string.encode('utf-8')).hexdigest()    
    
    print(hash_with_proof)

    # difficulty '0000' is easy
    # difficulty '00000' is extream hard
    if hash_with_proof[:5] == '00000':
    
        return 0
    
    else:
    
        return 1

proof = 0

while isvalidproof(proof):
    proof = proof + 1

print(proof)