import csv
import time
import sys
from attr import Attr

class CSVDiscretizer(object):

    def __init__(self, csv, new_csv):
        self.original_csv = 'csv_files/' + csv
        self.new_csv = 'csv_files/' + new_csv
        # A way to know how many different animal' species the csv has
        self.dog_breeds = set()
        self.cat_breeds = set()
        self.data = None
        self.populate_data_from_csv()
        self.discretize_ageuponoutcom()
        # self.discretize_breed_names()
        self.write_csv_file()

    """
    Populate data from original_csv in data
    """
    def populate_data_from_csv(self):
        with open(self.original_csv, 'rt') as csvfile:
            dictofdata = csv.DictReader(csvfile, delimiter=',')
            self.data = [{Attr.OutcomeType.value: row[Attr.OutcomeType.value], Attr.OutcomeSubtype.value: row[Attr.OutcomeSubtype.value], Attr.AnimalType.value: row[Attr.AnimalType.value],
                    Attr.SexuponOutcome.value: row[Attr.SexuponOutcome.value], Attr.AgeuponOutcome.value: row[Attr.AgeuponOutcome.value], Attr.Breed.value: row[Attr.Breed.value],
                    Attr.Color.value: row[Attr.Color.value]} for row in dictofdata]
            print("Quantidade de tuplas importadas do {}: {}".format(self.original_csv, len(self.data)))

    """
    Method to insert None in empty values:columns
    """
    def _discretize_empty_values(self):
        for animal_data in self.data:
            for k, v in animal_data.items():
                if v == '' or v == ' ':
                    animal_data[k] = None
        print('Done: _discretize_empty_values')

    """
    Method to discretize the value AgeuponOutcome, which cames as year, months or weeks
    """
    def discretize_ageuponoutcom(self):
        for animal_data in self.data:
            if animal_data[Attr.AgeuponOutcome.value]:
                if 'year' or 'years' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 365
                elif 'month' or 'months' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 30
                elif 'weeks' or 'week' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 7
                elif 'day' or 'days' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 7
                animal_data[Attr.AgeuponOutcome.value] = int(animal_data[Attr.AgeuponOutcome.value][0]) * day_multiplier
        print('Done: discretize_ageuponoutcom')

    """
    Method to discretize and normalize dog breed's names. It consists in finding and editing breeds' names with "Mix" and "/" by their first name.
    """
    def discretize_breed_names(self):
        for animal_data in self.data:
            if animal_data[Attr.AnimalType.value] == 'Dog':
                self.dog_breeds.add(animal_data[Attr.Breed.value])

        print(len(self.dog_breeds))
        for breed_animal in sorted(self.dog_breeds):
            string_match = breed_animal.find('/')
            string_match_2 = breed_animal.find(' Mix')
            if string_match != -1:
                self.dog_breeds.add(breed_animal[:string_match])
                print(breed_animal[:string_match])
                self.dog_breeds.discard(breed_animal) 
                print(breed_animal)
            elif string_match_2 != -1:
                self.dog_breeds.add(breed_animal[:string_match_2])
                self.dog_breeds.discard(breed_animal)

        print(len(self.dog_breeds))
        input()
    
    """
    Method to write self.data in new csv file
    """
    def write_csv_file(self):
        self._discretize_empty_values()
        with open(self.new_csv, 'wt') as outcsv:
            writer = csv.DictWriter(outcsv, fieldnames = [Attr.OutcomeType.value, Attr.OutcomeSubtype.value, Attr.AnimalType.value, Attr.SexuponOutcome.value, Attr.AgeuponOutcome.value, 
                                                          Attr.Breed.value, Attr.Color.value, Attr.Lifespan.value, Attr.Adaptability.value, Attr.Size.value])
            writer.writeheader()
            writer.writerows(self.data)
        print('Done: write_csv_file')


if __name__ == '__main__':
    csv_disc = CSVDiscretizer('train.csv', 'teste_1.csv')

