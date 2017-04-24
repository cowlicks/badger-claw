#!/usr/bin/env python

from collections import defaultdict
import json
import os
from pprint import pprint
import sys


def load(data_location):
    with open(data_location) as f:
        data = f.readlines()
    pprint("Loaded data from %s " % data_location)
    return json.loads(''.join(data))


def analyze(data):
    action_counts = defaultdict(int)
    for k, v in data['action_map'].items():
        action_counts[v['heuristicAction']] += 1

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

    analysis_results = {
            'action_counts': action_counts,
            'tracker_host_count': tracker_host_count,
            'snitch_counts': snitch_counts,
            'supercookie_counts':  len(data['supercookie_domains']),
            'supercookies_with_cookieblocks': len(set(data['supercookie_domains']) & set(cookieblocks)),
            'supercookies_with_blocks': len(set(data['supercookie_domains']) & set(blocks)),
            }
    pprint("Data analyzed, here's what we got:")
    pprint(analysis_results)
    return analysis_results


def save(out_location, data):
    with open(out_location, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    pprint("Saved analysis to %s" % out_location)


def main():
    data_location = sys.argv[1] or 'results.json'
    data = load(data_location)
    results = analyze(data)

    data_path, data_file = os.path.split(data_location)
    out_location = os.path.join(data_path, 'analysis-' + data_file)
    save(out_location, results)


if __name__ == '__main__':
    main()
