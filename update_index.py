#!/usr/bin/env python
import sys
import json

new_item = sys.argv[1]

index_location = 'results/index.json'
with open(index_location, 'r') as f:
    index = json.load(f)

index['index'].insert(0, new_item)

with open(index_location, 'w') as f:
    f.write(json.dumps(index, indent=4, sort_keys=True))

print('Index updated')
