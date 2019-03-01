from pprint import pprint
from witness_monitor.config import config
from witness_monitor.features import Feature
from witness_monitor import Monitor

from witness_monitor.features.block_production import Block_production


m = Monitor(config)
m.test()

print("Failures")
print("=" * 80)
pprint(Feature.get_failures())
print("Successes")
print("=" * 80)
pprint(Feature.get_successes())
