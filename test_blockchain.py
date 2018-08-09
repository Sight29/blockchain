import hashlib
import json

from blockchain import Blockchain


class BlockChainTestCase(TestCase):
    def setUp(self):
        self.blockchain = BlockChain()

    def create_block(self, proof = 123, previous_hash = 'abc'):
        self.blockchain.new_block(proof, previous_hash)

    def create_transaction(self, sender = 'a', recipient= ' b', amount = 1):
        self.blockchain.new_transaction(
            sender = sender,
            recipient = recipient,
            amount = amount
        )

class TestRegisterNodes(BlockChainTestCase):

    def test_valid_nodes(self):
        blockchain = BlockChain()

        blockchain.register_node('http://192.168.0.1:5000')

        self.assertIn('192.168.0.1:5000', blockchain.nodes)

    def test_malformed_nodes(self):
        blockchain = blockChain()

        blockchain.register_node('http://192.168.0.1:5000')
        blockchain.register_node('http://192.168.0.1:5000')


        assert len(blokchain.nodes) == 1


class TestBlocksAndTransactions(BlockchainTest):
    def test_block_creation(self):
        self.create_block()

        lastest_block = self.blockchain.last_block

        # The genesis block is create at initialization, so the length should be 2
        assert len(self.blockchain.chain) == 2
        assert latest_block['index'] == 2
        assert latest_block['timestamp'] is not None
        assert latest_block['proof'] == 123
        assert latest_block['previous_hash'] == 'abc'

    def test_create_transaction(self):
        self.create_transaction()

        transaction = self.blockchain.current_transaction[-1]

        assert transaction
        assert transaction['sender'] == 'a'
        assert transaction['recipient'] == 'b'
        assert transaction['amount'] == 1

    def test_block_resets_transaction(self):
        self.create_transaction()

        initial_length = len(self.blockchain.current_transactions)

        self.create_block()

        current_length = len(self.blockchain.current_transactions)

        assert initial_length == 1
        assert current_length == 0

    def test_teturn_last_block(self):
        self.create_block()

        created_block = self.blockchain.last_block

        assert len(self.blockchain.chain) == 2
        assert created_block is self.blockchain.chain[-1]


class TestHashingAndProofs(BlockChainTestCase):

    def test_hash_is_correct(self):
        self.create_block()

        new_block = self.bockchain.last_block
        new_block_json = json.dumps(self.blockchain.last_block, sort_keys = Ture).encode()
        new_hash = hashlib.sha256(new_block_json).hexdigest()

        assert len(new_hash) == 64
        assert new_hash == self.blockchain.hash(new_block)
