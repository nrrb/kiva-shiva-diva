from __future__ import unicode_literals
import unicodecsv
import json
import glob
import sys
import os
import re

JSON_DATA_PATH = './data'
CSV_PATH = './csv'

FILENAME_PATTERN = re.compile(r'(?P<lender_id>[^_.]*)')
def lender_id_from_filename(filename):
    filename = os.path.basename(filename)
    return re.search(FILENAME_PATTERN, filename).groupdict()['lender_id']

def parse_json_loan(loan):
    record = {
        'loan_id': loan['id'],
        'activity': loan['activity'],
        'borrower_count': loan['borrower_count'],
        'funded_amount': loan['funded_amount'],
        'image_id': loan['image']['id'],
        'loan_amount': loan['loan_amount'],
        'country': loan['location']['country'],
        'country_code': loan['location']['country_code'],
        'borrower_name': loan['name'],
        'partner_id': loan['partner_id'],
        'posted_date': loan['posted_date'],
        'sector': loan['sector'],
        'status': loan['status'],
        'use': loan['use']
    }
    return record

def json_to_csv(json_filename, csv_filename):
    with open(json_filename, 'rb') as f:
        data = json.load(f)

    lender_id = lender_id_from_filename(json_filename)

    loans = [parse_json_loan(loan) for loan in data['loans']]
    if len(loans) == 0:
        return

    for i in xrange(len(loans)):
        loans[i]['lender_id'] = lender_id

    with open(csv_filename, 'wb') as f:
        # Hopefully all loans have the same keys - use validator to check first
        writer = unicodecsv.DictWriter(f, fieldnames=sorted(loans[0].keys()))
        writer.writeheader()
        writer.writerows(loans)


if __name__ == "__main__":
    print("Finding files to process...")
    json_filenames = glob.glob(os.path.join(JSON_DATA_PATH, '*.json'))
    print("Found {n} files. Now finding files already processed...".format(n=len(json_filenames)))
    csv_filenames = glob.glob(os.path.join(CSV_PATH, '*.csv'))
    print("Found {n} files.".format(n=len(csv_filenames)))
    csv_filenames = sorted(csv_filenames)
    json_bases = []
    csv_bases = []
    for filename in json_filenames:
        base, _ = os.path.splitext(os.path.basename(filename))
        json_bases.append(base)
    for filename in csv_filenames:
        base, _ = os.path.splitext(os.path.basename(filename))
        csv_bases.append(base)
    json_bases = list(set(json_bases) - set(csv_bases))
    json_filenames = [os.path.join(JSON_DATA_PATH, base + '.json') for base in json_bases]
    print("{n} remaining files to download.".format(n=len(json_filenames)))
    _ = raw_input()
    for filename in json_filenames:
        base, _ = os.path.splitext(os.path.basename(filename))
        csv_file = os.path.join(CSV_PATH, base + '.csv')
        json_to_csv(filename, csv_file)
        print('{f1} => {f2}'.format(f1=filename, f2=csv_file)) 

