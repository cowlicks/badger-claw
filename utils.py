import json
import subprocess

from logger import logger


def save_json(out_name, out_data):
    with open(out_name, 'w') as f:
        f.write(json.dumps(out_data, indent=4, sort_keys=True))
    logger.info('Data saved successfully to %s' % out_name)


def get_git_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode('utf-8')


def get_date_time():
    return subprocess.check_output(["date",  "+%Y_%m_%d_%I_%M_%p"]).strip().decode('utf-8')


def update_index(new_item):
    index_location = 'results/index.json'
    with open(index_location, 'r') as f:
        index = json.load(f)

    index['index'].insert(0, new_item)

    save_json(index_location, index)
    logger.info('Index updated')


def save_everything(commit, datetime, out_data):
    results_file = 'results-' + commit + '-' + datetime + '.json'
    results_location = 'results/' + results_file

    save_json(results_location, out_data)
    update_index(results_file)
