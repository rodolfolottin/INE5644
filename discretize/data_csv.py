import csv
import settings
from attr import Attr


class CSV(object):

    def __init__(self, origin_csv, params = list(), should_return=False):
        self.csv_file = settings.CSV_PATH + origin_csv
        self.params = params
        self.csv_data = None
        if should_return:
            self.csv_data = self.read_data_from_csv()

    def read_data_from_csv(self):
        with open(self.csv_file, 'rt') as r_csv:
            data = csv.DictReader(r_csv, delimiter=',')
            csv_data = []
            for line in data:
                info = {}
                for param in self.params:
                    info[param.value] = line[param.value]
                csv_data.append(info)
        print('Done: {}, {}'.format(self.read_data_from_csv.__name__, self.csv_file))
        return csv_data

    def create_new_csv(self, csv_filename, data):
        final_params = [k for k in data[0]]
        with open(settings.CSV_PATH + csv_filename, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, fieldnames = final_params)
            writer.writeheader()
            writer.writerows(data)
        print('Done: {csv}. New csv file created: {path}'.format(csv=self.create_new_csv.__name__, path=settings.CSV_PATH + csv_filename))

