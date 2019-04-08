from .abstractaction import Action
from bitshares.instance import shared_blockchain_instance


class DisapproveWitness(Action):

    __tag__ = "disapprove_witness"

    def fire(self, witness):
        bitshares = shared_blockchain_instance()
        account = self.config.get("voter")
        bitshares.disapprovewitness(witness, account=account)
