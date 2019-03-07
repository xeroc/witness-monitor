from pprint import pprint
from .abstractfeature import Feature
from ..storage import Base, session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


class BlockProductionCache(Base):
    __tablename__ = "blockproductioncache"
    id = Column(Integer, primary_key=True)
    witness = Column(String(50))
    key = Column(String(50))
    value = Column(Text)


class Block_production(Feature):
    __tag__ = "block_production"

    def test(self, witness):
        w = self.data["witness"].get(witness)
        if not w:
            return
        missed = float(w["total_missed"] or 0)
        cached = float(self.from_cache(witness, "total_missed") or 0)
        if cached:
            difference = missed - cached
            if difference > self.params.get("max_misses", 5):
                self.failure(
                    witness,
                    error=dict(total_missed=missed, since_last_check=difference),
                )
            else:
                self.success(witness, total_missed=missed, since_last_check=difference)
        self.to_cache(witness, "total_missed", missed)

    def to_cache(self, witness, key, value):
        entry = (
            session.query(BlockProductionCache)
            .filter_by(witness=witness, key=key)
            .first()
        )
        if entry:
            entry.value = value
        else:
            x = BlockProductionCache()
            x.value = value
            x.key = key
            x.witness = witness
            session.add(x)
        session.commit()

    def from_cache(self, witness, key):
        return (
            session.query(BlockProductionCache.value)
            .filter_by(witness=witness, key=key)
            .scalar()
        )
