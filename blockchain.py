import hashlib as hasher
import time


class Message:
    def __init__(self, data):
        self.hash = None
        self.prev_hash = None
        self.timestamp = time.time()
        self.data = data
        self.hash_time_data = self._hash_time_data()

    def _hash_with_prev(self):
        return hasher.sha256(bytearray(str(self.prev_hash) + self.hash_time_data, "utf-8")).hexdigest()

    def _hash_time_data(self):
        return hasher.sha256(bytearray(str(self.timestamp) + str(self.data), "utf-8")).hexdigest()

    def copy_prev_hash(self, message):
        """ Link a block to the previous block."""
        self.prev_hash = message.hash

    def full_hash(self):
        self.hash = self._hash_with_prev()

    def validate(self):
        """ Check whether the message is valid or not. """
        if self.hash_time_data != self._hash_time_data():
            raise InvalidMessage("Invalid payload hash in message: " + str(self))
        if self.hash != self._hash_with_prev():
            raise InvalidMessage("Invalid message hash in message: " + str(self))

    def __repr__(self):
        return 'Message<hash: {}, prev_hash: {}, data: {}>'.format(
            self.hash, self.prev_hash, self.data
        )

class Block:
    def __init__(self):
        self.messages = None
        self.timestamp = None
        self.prev_hash = None
        self.hash = None

    def _hash_block(self):
        return hasher.sha256(
            bytearray(str(self.prev_hash) + str(self.timestamp) + self.messages.hash, "utf-8")).hexdigest()

    def add_message(self, data):
        self.messages = Message(data)
        self.messages.full_hash()
        self.messages.validate()

    def update_message(self, data):
        self.messages = Message(data)
        self.messages.full_hash()
        self.messages.validate()

    def link(self, block):
        self.prev_hash = block.hash

    def full_hash(self):
        self.timestamp = time.time()
        self.messages.full_hash()
        self.hash = self._hash_block()

    def validate(self):
        self.messages.validate()

    def __repr__(self):
        return 'Block<hash: {}, prev_hash: {}, time: {}. {}>'.format(
            self.hash, self.prev_hash, self.timestamp, self.messages
        )


class HistoryChain:
    def __init__(self):
        self.chain = []

    def add_block(self, block):
        if len(self.chain) > 0:
            block.prev_hash = self.chain[-1].hash
            block.messages.prev_hash = self.chain[-1].messages.hash
        block.full_hash()
        block.validate()
        self.chain.append(block)

    def validate(self):
        """ Validates each block in order"""
        if len(self.chain) > 1:
            for i, block in enumerate(self.chain):
                if i < len(self.chain) - 1:
                    if self.chain[i].messages.hash != self.chain[i+1].messages.prev_hash:
                        raise InvalidBlockchain("Invalid blockchain due to different message hash between blocks {} & {}.".format(i, i+1))
        print("Blockchain integrity validated.")
        return True

    def printChain(self):
        for block in self.chain:
            print(block)
            print("-------------")

    def __repr__(self):
        return 'SimpleChain<blocks: {}>'.format(len(self.chain))


class InvalidMessage(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidBlock(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class InvalidBlockchain(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def manager():
    chain = HistoryChain()
    block = Block()
    msg = """
		Basic implementation of a Blockchain. Changes are inmutable. Be aware.
		Action set:
			- add message to the existing block  (1)
			- add existing block to the chain    (2)
			- show a block (index will be asked) (3)
			- show the whole chain               (4)
			- validate the chain integrity       (5)
			- update message in block            (6)
			- exit the program                   (7)
		The validate action will kill the program if the integrity of the chain
		is compromised.
		"""

    print(msg)
    while True:
        print()

        decide = input("Your action: ")

        if decide == "1":
            block.add_message(input("Enter your data: "))
        elif decide == "2":
            if block.messages is not None:
                chain.add_block(block)
                block = Block()
            else:
                print("Block is empty.")
        elif decide == "3":
            index = int(input("Provide the index: "))
            if len(chain.chain) > 0:
                try:
                    print(chain.chain[index])
                except:
                    print("An issue occurred.")
        elif decide == "4":
            for b in chain.chain:
                print(b)
                print("----------------")
        elif decide == "5":
            if chain.validate(): print("Integrity validated.")
        elif decide == "6":
            print(len(chain.chain))
            index = int(input("Provide index of block to be updated: "))
            chain.chain[index].update_message(input("Enter new data: "))

        else:
            break


if __name__ == "__main__":
    manager()