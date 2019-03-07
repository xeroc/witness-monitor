import math
from ..utils import convert_to_timedelta
from .abstractfeature import Feature
from datetime import datetime, timedelta
from bitshares.price import PriceFeed, Price


class FeedParameter(Feature):
    def test(self, witness):
        feeds = self.data.get("feed", {})
        for symbol in self.config.get("assets"):
            asset_feed = feeds.get(symbol)
            if symbol in self.params.get("assets", []):
                self.test_asset(witness, symbol, asset_feed)

    def test_asset(self, witness, symbol, asset_feed):
        if not asset_feed:
            return
        for feed in asset_feed:
            producer = feed.get("producer")
            if self.data["account"][witness]["id"] == producer["id"]:
                self.test_feed(witness, symbol, feed)


class Feed_mcr(FeedParameter):
    __tag__ = "feed_mcr"

    default_max = 200
    default_min = 101

    def test_feed(self, witness, symbol, feed):
        # rfeed = self.data["asset"][symbol]["bitasset_data"]["current_feed"]
        # rmcr = float(rfeed["maintenance_collateral_ratio"] / 10)
        _max = self.params.get("max", self.default_max)
        _min = self.params.get("min", self.default_min)
        mcr = float(feed["maintenance_collateral_ratio"] / 10)

        if mcr > _max or mcr < _min:
            self.failure(witness, min=_min, max=_max, value=mcr)
        else:
            self.success(witness, min=_min, max=_max, value=mcr)


class Feed_mssr(FeedParameter):
    __tag__ = "feed_mssr"

    default_max = 115
    default_min = 101

    def test_feed(self, witness, symbol, feed):
        # rfeed = self.data["asset"][symbol]["bitasset_data"]["current_feed"]
        # rmcr = float(rfeed["maximum_short_squeeze_ratio"] / 10)
        _max = self.params.get("max", self.default_max)
        _min = self.params.get("min", self.default_min)
        mssr = float(feed["maximum_short_squeeze_ratio"] / 10)

        if mssr > _max or mssr < _min:
            self.failure(witness, min=_min, max=_max, value=mssr)
        else:
            self.success(witness, min=_min, max=_max, value=mssr)


class Feed_age(FeedParameter):
    __tag__ = "feed_age"

    default_max_age = "1d"

    def test_feed(self, witness, symbol, feed):
        date = feed["date"].replace(tzinfo=None)
        now = datetime.utcnow()
        d = convert_to_timedelta(self.params.get("max", self.default_max_age))

        if now - d > date:
            self.failure(witness, age=(now - date).seconds)
        else:
            self.success(witness, age=(now - date).seconds)


class Feed_price(FeedParameter):
    __tag__ = "feed_settlementprice"

    default_max_age = "1d"

    def test_feed(self, witness, symbol, feed):
        current_feed = self.data["asset"][symbol]["bitasset_data"]["current_feed"]
        pw = feed["settlement_price"]
        p = Price(current_feed["settlement_price"])

        def diff_percentage(p, pw):
            return math.fabs((float(pw) - float(p)) / float(p) * 100)

        param = self.params.get("diff_percentage")
        if param:
            max = float(param.get("max"))
            if max:
                if max < diff_percentage(p, pw):
                    self.failure(witness, diff_percentage=diff_percentage(p, pw))

        if not self.failed:
            self.success(witness)
