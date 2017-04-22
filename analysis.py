#!/usr/bin/env python
'''
It'd be interesting to know what cookie values are the biggest culprits.
'''
from collections import defaultdict
import json
from pprint import pprint as print

with open('results.json') as f:
    data = f.readlines()
data = json.loads(''.join(data))

action_counts = defaultdict(int)
for k, v in data['action_map'].items():
    action_counts[v['heuristicAction']] += 1
print(action_counts)


snitch_counts = defaultdict(int)
tracker_hosts = defaultdict(int)
for k, v in data['snitch_map'].items():
    snitch_counts[len(v)] += 1
    for tracker in v:
        tracker_hosts[tracker] += 1

tracker_host_count = defaultdict(int)
for k, v in tracker_hosts.items():
    tracker_host_count[v] += 1

cookieblocks = [k for k, v in data['action_map'].items() if v['heuristicAction'] == 'cookieblock']
blocks = [k for k, v in data['action_map'].items() if v['heuristicAction'] == 'block']

print('tracker host count')
print(tracker_host_count)
print('snitch_counts')
print(snitch_counts)
print('supercookie counts')
print(len(data['supercookie_domains']))
# fortune.com has 35 trackers!!
# optimizely is seen on 29 sites!! 

print('supercookies with cookieblocks')
print(len(set(data['supercookie_domains']) & set(cookieblocks)))
print('supercookies with blocks')
print(len(set(data['supercookie_domains']) & set(blocks)))
