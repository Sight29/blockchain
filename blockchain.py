# This class is resposible for managing the chain. It will store tranasctions and
# have some helper methods for adding new blocks to the chain.

import hashlib
import json
from time import time
from uuid import uuid4


import requests
from flask import Flask, jsonify, request


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.current_transaction = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):

        """
        Add a new node the list of nodes

        :param address: Address of node. Eg. 'http://192.168,0,5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like 192.168.0.5:5000.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain in valid

        :param chain: A BlockChain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            printf(f'{last_block}')
            printf(f'{block}')
            printf("\n---------------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflict(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain ws replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're onlt looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all then nodes in out network
        for node in neighbours:
            response = reqests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer tan the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longet than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False


    def new_block(self):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the proof of work algorithm
        :param previous_block: Hash of previous block
        :return: New Block
        """
        block = {
            'index': len(self.chain)+ 1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hsh(self.chain[-1]),
        }

        # Reset the current list of the tranasctions
        self.current_transaction = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a anew transcation to go into the net mined block

        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipien
        :param amount: <int> Amount
        :return: <int> The index of the block that will old this transactions
        """

        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        """
        Creayes a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys = true).encode()
        return hashlib.sha256(block_string).hexdigest()



    @staticmethod
    def last_block(self):
        # Return the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_block):
        """
        Simple proof of work algorithm

        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p
        is the previous p'
        - p is the previous proof, and p' is the new proof.

        :param last_proof: <int>
        :Return : <int>
        """
        last_proof = last_block['proof']
        last_hash  = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is false:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the proof

        :param last_proof: <int> Previous proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The has hof the previous block
        :return: <bool> True if correct, false if not.

       """

       guess = f'{lazst_proof}{proof}{last_hash}'.encode()
       guess_hash = hashlib.sha256(guess).hexdigest()
       return guess_hash[:4] == "0000"




    # Instantiate the Node
    app = Flask(__name__)

    # Generate a globally unique address for this node
    node_indentifier = str(uuid4()).replace('-'m '')

    # Instantiate the blockchain
    blockchain = Blockchain()

    @app.route('/mine', methods=['GET'])
    def mine():
        # We run the proof of work algorithm to get the next proof
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to singify that this node has mined a new coin.
        blockchain.new_transaction(
            sender = "0",
            recipient = node_indentifier,
            amount = 1,
        )

        # Forge the new block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transcations': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify{response}, 200


    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()

        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all (k in values for k in required):
            return 'Missing values', 400

        # Creates a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    @app.route('/chain', methods = ['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


    @app.route('/nodes/register', methods = ['POST'])
    def register_nodes():
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400


        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }
        return jsonify(response), 201


    @app.route('/nodes/resolve', methods = ['GET'])
    def consensus():
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        return jsonify(response), 200

    if __name__ == '__main__':
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument('-p', '--port', default = 5000, type = int, help = 'port to listne on')
        args = parser.parse_args()
        port = args.port

        app.run(host='0.0.0.0', port = port)
