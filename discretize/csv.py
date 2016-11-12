import csv
from attr import Attr

CSV_PATH = '../csv_files/'

class CSV(object):

    def __init__(self, csv, list: params):
        self.csv_file = CSV_PATH + csv
        self.params = params

    def read_data_from_csv(self):
        with open(self.csv_file, 'rt') as r_csv:
            data = csv.DictReader(r_csv, delimiter=',')
            self.breed_info = [{param: line[param] for param in self.params}] for line in data]
    print('Done: {}'.format(csv=self.read_data_from_csv.__name__)

    def create_new_csv(self, csv_filename, data):
            with open(CSV_PATH + csv_filename, 'rt') as new_csv:
                writer = csv.DictWriter(new_csv, filenames = self.params)
                writer.writeheader()
                writer.writerows(data)
        print('Done: {}. New csv file created: {}'.format(csv=self.create_new_csv.__name__, path=CSV_PATH + csv_filename)

