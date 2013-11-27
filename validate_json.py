# This doesn't work
import json
from random import choice
import os
import glob

DATA_PATH = './data'
FILES_TO_TEST = 100

def validate_json_schema(data, schema):
    """
    Given two JSON data structures, data and schema, this checks that all keys that are in 
    schema are also in data and that all values referred to by those keys in the schema also
    exist in data and are of the same Python data type.
    """
    is_json_valid = True
    if type(data) != type(schema):
        is_json_valid = False
        return is_json_valid
    elif type(schema) == list:
        is_json_valid &= all([validate_json_schema(item, schema[0]) for item in data])
        return is_json_valid
    elif type(schema) == dict:
        for k, v in schema.iteritems():
            if k not in data:
                return False
            if type(data[k]) != type(v):
                return False
            is_json_valid &= validate_json_schema(data[k], v)
            return is_json_valid
    else:
        return True


if __name__ == "__main__":
    with open('loan_schema.json', 'rb') as f:
       loan_schema = json.load(f)
    def validate_json(data):
        return validate_json_schema(data, loan_schema)

    print('Getting list of data files...')
    filenames = glob.glob(os.path.join(DATA_PATH, '*.json'))
    print('Found {n} data files. Testing {m} of them.'.format(n=len(filenames), m=FILES_TO_TEST))

    for _ in xrange(FILES_TO_TEST):
        filename = choice(filenames)
        with open(filename, 'rb') as f:
            data = json.load(f)
        if len(data['loans']) > 0:
            v = all(map(validate_json, data['loans']))
            if v:
                print('{f} is valid.'.format(f=filename))
            else:
                print('{f} is INVALID.'.format(f=filename))
