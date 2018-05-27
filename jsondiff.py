import json
import sys

from util import json_util
from util import str_util


def flatten_json(json_val):
    # nested json values are flattened and stored as key-value pairs
    flat_json = {}

    def explore_each(json_val, key_list):
        if isinstance(json_val, dict):
            for key, val in json_val.items():
                explore_each(val, key_list + [key])
        else:
            flat_json['.'.join(key_list)] = json_val

    explore_each(json_val, [])
    return flat_json


def compare_joined_flat_json(joined):
    for key, val in joined.items():
        val_A, val_B = val
        if val_A != val_B:
            diffs = []
            if val_A:
                diffs.append(str_util.colorize(
                    "- {key}: {val}".format(key=key, val=val_A), 'red'))
            if val_B:
                diffs.append(str_util.colorize(
                    "+ {key}: {val}".format(key=key, val=val_B), 'green'))

            print('\n'.join(diffs))
            print("---")


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 3:
        print("Usage: python {} A.json B.json".format(argvs[0]))
        sys.exit(1)

    _, json_file_A, json_file_B = argvs
    with open(json_file_A) as f:
        json_A = json.load(f)
    with open(json_file_B) as f:
        json_B = json.load(f)

    flat_json_A = flatten_json(json_A)
    flat_json_B = flatten_json(json_B)
    joined_json = json_util.join_json_by_key(flat_json_A, flat_json_B)

    compare_joined_flat_json(joined_json)
