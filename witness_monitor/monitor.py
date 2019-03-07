from bitshares.asset import Asset
from bitshares.witness import Witness
from .features import Feature
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
        for witness_name in self.config.get("witnesses"):
            witness = Witness(witness_name)
            self.data["witness"][witness_name] = witness
            self.data["account"][witness_name] = witness.account

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
                for witness in self.config.get("witnesses"):
                    k.test(witness)


Base.metadata.create_all(engine)
