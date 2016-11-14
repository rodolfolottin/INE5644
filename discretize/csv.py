import csv
import settings
from attr import Attr


class CSV(object):

    def __init__(self, csv, params = list(), should_return=False):
        self.csv_file = settings.CSV_PATH + csv
        self.params = params
        if should_return:
            return self.read_data_from_csv()

    def read_data_from_csv(self):
        with open(self.csv_file, 'rt') as r_csv:
            data = csv.DictReader(r_csv, delimiter=',')
            csv_data = []
            for line in data:
                info = {}
                for param in self.params:
                    info[param] = line[param]
                csv_data.append(info)
        print('Done: {}'.format(csv=self.read_data_from_csv.__name__))
        return csv_data

    def create_new_csv(self, csv_filename, data):
        final_params = [k for k in data[0]]
        with open(settings.CSV_PATH + csv_filename, 'rt') as new_csv:
            writer = csv.DictWriter(new_csv, filenames = final_params)
            writer.writeheader()
            writer.writerows(data)
        print('Done: {}. New csv file created: {}'.format(csv=self.create_new_csv.__name__, path=settings.CSV_PATH + csv_filename))

