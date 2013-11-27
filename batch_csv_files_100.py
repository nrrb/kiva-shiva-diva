from itertools import islice
import unicodecsv
import glob

BATCHES = 100
fieldnames = [u'lender_id', u'loan_id', u'activity', u'borrower_count', u'borrower_name', u'country', u'country_code', u'funded_amount', u'image_id', u'loan_amount', u'partner_id', u'posted_date', u'sector', u'status', u'use']

if __name__ == "__main__":
    print('Getting list of CSV files...')
    csv_files = glob.glob('./csv/*.csv')
    print('Found {n} files. Splitting into {b} batches (maybe an extra!).'.format(
        n=len(csv_files), b=BATCHES)
    
    for start in xrange(BATCHES):
        output_filename = './csv_batch_100/batch{0}.csv'.format(start+1)
        print('Creating batch CSV file {0}.'.format(output_filename))
        with open(output_filename, 'wb') as f_out:
            dict_writer = unicodecsv.DictWriter(f_out, fieldnames=fieldnames)
            dict_writer.writeheader()
            for csv_file in islice(csv_files, start, None, BATCHES):
                with open(csv_file, 'rb') as f_in:
                    dict_writer.writerows(list(unicodecsv.DictReader(f_in)))
        

