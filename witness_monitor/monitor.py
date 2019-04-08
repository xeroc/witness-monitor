from bitshares.account import Account
from bitshares.asset import Asset
from bitshares.witness import Witness
from .features import Feature
from .actions import Action
from .storage import Base, engine


class Monitor:
    def __init__(self, config):
        self.config = config
        self.data = dict(asset={}, feed={}, witness={}, account={})
        self._loadchaindata()

    def _loadchaindata(self):
        for symbol in self.config.get("assets"):
            asset = Asset(symbol, full=True)
            self.data["asset"][symbol] = asset
            self.data["feed"][symbol] = asset.feeds
        for witness_name in self.witnesses:
            witness = Witness(witness_name)
            self.data["witness"][witness_name] = witness
            self.data["account"][witness_name] = witness.account

    @property
    def witnesses(self):
        voter = self.config.get("voter")
        if not voter:
            return []
        witnesses = list()
        account = Account(voter, full=True)
        for vote in account["votes"]:
            if "witness_account" not in vote:
                continue
            witnesses.append(Account(vote["witness_account"])["name"])
        return witnesses

    """ Tests
    """

    def test(self, features=[]):
        if not features:
            features = self.config.get("features")

        for feature in features:
            self.test_feature(feature)

    def test_feature(self, feature):
        for key, value in feature.items():
            klass = Feature.get_class(key)
            if klass:
                k = klass(feature=feature, config=self.config, data=self.data)
                for witness in self.witnesses:
                    k.test(witness)

    """ Actions
    """

    def action(self):
        results = list()
        for success in Feature.get_successes():
            results.append(success)

        for failure in Feature.get_failures():
            results.append(failure)

        for result in results:
            witness = result["witness"]
            actions = result["actions"]
            if not actions:
                continue

            for action in actions:
                klass = Action.get_class(action)
                if not klass:
                    continue
                k = klass(action=action, config=self.config, result=result)
                k.fire(witness)


Base.metadata.create_all(engine)
