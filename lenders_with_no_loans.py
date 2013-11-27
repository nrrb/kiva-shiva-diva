import glob
import json
import re
import os

JSON_DATA_PATH = './data'

FILENAME_PATTERN = re.compile(r'(?P<lender_id>[^_.]*)')
def lender_id_from_filename(filename):
    filename = os.path.basename(filename)
    return re.search(FILENAME_PATTERN, filename).groupdict()['lender_id']

if __name__ == "__main__":
   json_filenames = glob.glob(os.path.join(JSON_DATA_PATH, '*.json'))
   for json_filename in json_filenames:
       with open(json_filename, 'rb') as f:
           data = json.load(f)
       if data['paging']['total'] == 0:
            print(lender_id_from_filename(json_filename))
