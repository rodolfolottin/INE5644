import csv
import time
import sys
from attr import Attr

class CSVDiscretize(object):

    def __init__(self, csv, new_csv, one_way=True):
        self.original_csv = 'csv_discs/' + csv
        self.new_csv = 'csv_discs/' + new_csv
        # A way to know how many different animal' species the csv has
        self.dog_breeds = set()
        self.cat_breeds = set()
        self.data = None
        self.breed_info = None
        if one_way:
            self.populate_data_from_csv(self.original_csv)
            self._discretize_empty_values()
            self.discretize_ageuponoutcom()
            self.discretize_breed_names()
            self.populate_breed_from_csv()
            self.merge_breed_with_tuples()
            self.discretize_size()
            self.create_intervals()

    """
    Popula data de csv
    """
    def populate_data_from_csv(self, csv_disc, should_return=False):
        with open(csv_disc, 'rt') as csvfile:
            dictofdata = csv.DictReader(csvfile, delimiter=',')
            self.data = [{Attr.AnimalType.value: row[Attr.AnimalType.value],
                    Attr.SexuponOutcome.value: row[Attr.SexuponOutcome.value], Attr.AgeuponOutcome.value: row[Attr.AgeuponOutcome.value], Attr.Breed.value: row[Attr.Breed.value],
                    Attr.Color.value: row[Attr.Color.value]} for row in dictofdata]
# para o train.csv
#self.data = [{Attr.OutcomeType.value: row[Attr.OutcomeType.value], Attr.AnimalType.value: row[Attr.AnimalType.value],
#                    Attr.SexuponOutcome.value: row[Attr.SexuponOutcome.value], Attr.AgeuponOutcome.value: row[Attr.AgeuponOutcome.value], Attr.Breed.value: row[Attr.Breed.value],
#                    Attr.Color.value: row[Attr.Color.value]} for row in dictofdata]

            print("Quantidade de tuplas importadas do {}: {}".format(csv_disc, len(self.data)))
            if should_return:
                return self.data

    """
    Método para retirar elementos que não tenham todos valores preenchidos.
    """
    def _discretize_empty_values(self):
        retirar_elementos = []
        for animal_data in self.data:
            for k, v in animal_data.items():
                if v == '' or v == 'Unknown' or v == ' ' or v == 'Unknown':
                    retirar_elementos.append(animal_data)
        self.data = [x for x in self.data if x not in retirar_elementos]
        print(len(self.data))
        print('Done: _discretize_empty_values')

    """
    Método utilizado para discretizar o atributo AgeuponOutcome, que pode vir como semana, mês ou ano. Discretizado para dias.
    """
    def discretize_ageuponoutcom(self):
        for animal_data in self.data:
            if animal_data[Attr.AgeuponOutcome.value] and animal_data[Attr.AgeuponOutcome.value] != 'Unknown':
                if 'year' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 365
                elif 'month' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 30
                elif 'week' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 7
                elif 'day' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 1
                total_dias = int(animal_data[Attr.AgeuponOutcome.value][0]) * day_multiplier
                animal_data[Attr.AgeuponOutcome.value] = total_dias / 30
        print('Done: discretize_ageuponoutcom')

    """
    Método utilizado para discretizar e analisar raças de animais.
    """
    def discretize_breed_names(self):
        for animal_data in self.data:
            if animal_data[Attr.AnimalType.value] == 'Dog':
                self.dog_breeds.add(animal_data[Attr.Breed.value])
            elif animal_data[Attr.AnimalType.value] == 'Cat':
                self.cat_breeds.add(animal_data[Attr.Breed.value])
            else:
                print(animal_data[Attr.Breed.value])

        for animal_data in self.data:
            breed_animal = animal_data[Attr.Breed.value]
            string_match = breed_animal.find('/')
            string_match_2 = breed_animal.find(' Mix')
            string_match_3 = breed_animal.find('Hound')
            if 'Black/Tan Hound Mix' in breed_animal:
                animal_data[Attr.Breed.value] = 'Black and Tan Coonhound'
            elif string_match != -1:
                animal_data[Attr.Breed.value] = breed_animal[:string_match]
            elif string_match_2 != -1:
                animal_data[Attr.Breed.value] = breed_animal[:string_match_2]

            # Normalizando alguns nomes
            if animal_data[Attr.Breed.value] == 'Redbone Hound':
                animal_data[Attr.Breed.value] = 'Redbone Coonhound'

            if animal_data[Attr.Breed.value] == 'Bluetick Hound':
                animal_data[Attr.Breed.value] = 'Bluetick Coonhound'

            if animal_data[Attr.Breed.value] == 'American Pit Bull Terrier':
                animal_data[Attr.Breed.value] = 'Pit Bull'

            if animal_data[Attr.Breed.value] == 'Javanese':
                animal_data[Attr.Breed.value] = 'Japanese'

            if 'St. Bernard' in animal_data[Attr.Breed.value]:
                animal_data[Attr.Breed.value] = 'St. Bernard'

            if animal_data[Attr.Breed.value] == 'Queensland Heeler':
                animal_data[Attr.Breed.value] = 'Australian Cattle Dog'

            retirar_elementos = []
            if animal_data[Attr.Breed.value] == 'Unknown':
                retirar_elementos.append(animal_data)
                self.data = [x for x in self.data if x not in retirar_elementos]
                print(len(self.data))

        print('Done: discretize_breed_names')

    """
    Método utilizado para discretizar o atributo Size
    """
    def discretize_size(self):
        value = None
        for animal_data in self.data:
            try:
                if 'Small' == animal_data[Attr.Size.value]:
                    value = 'Small'
                elif 'Small to Medium' == animal_data[Attr.Size.value]:
                    value = 'Small'
                elif 'Medium' == animal_data[Attr.Size.value]:
                    value = 'Medium'
                elif 'Medium to Large' == animal_data[Attr.Size.value]:
                    value = 'Medium'
                elif 'Large' == animal_data[Attr.Size.value] or 'large' == animal_data[Attr.Size.value] or 'Largest' == animal_data[Attr.Size.value]:
                    value = 'Large'
                elif 'Large to Giant' == animal_data[Attr.Size.value]:
                    value = 'Large'
                elif 'Giant' == animal_data[Attr.Size.value]:
                    value = 'Giant'
                else:
                    print(animal_data[Attr.Size.value])
                    input()
            except Exception as e:
                print(animal_data)
                pass
            animal_data[Attr.Size.value] = value
        print('Done: discretize_size')

    """
    Método utilizado para gerar intervalos dos atributos AgeuponOutcome e Lifespan
    """
    def create_intervals(self):
         age_values = [animal[Attr.AgeuponOutcome.value] for animal in self.data]
         age_min_value = min(age_values)
         age_max_value = max(age_values)
         lifespan_values = []
         for animal in self.data:
             if animal[Attr.Lifespan.value]:
                 lifespan_values.append(animal[Attr.Lifespan.value])
         lifespan_min_value = min(lifespan_values)
         lifespan_max_value = max(lifespan_values)

         for x in self.data:
             if x[Attr.AgeuponOutcome.value] >= age_min_value and x[Attr.AgeuponOutcome.value] < age_max_value / 4:
                 value = '1'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value / 4 and x[Attr.AgeuponOutcome.value] < age_max_value / 2:
                 value = '2'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value / 2 and x[Attr.AgeuponOutcome.value] < age_max_value - (age_max_value / 4):
                 value = '3'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value - (age_max_value / 4):
                 value = '4'
             x[Attr.AgeuponOutcome.value] = value

         for x in self.data:
             if x[Attr.Lifespan.value] >= lifespan_min_value and x[Attr.Lifespan.value] < lifespan_max_value / 4:
                 value = '1'
             elif x[Attr.Lifespan.value] >= lifespan_max_value / 4 and x[Attr.Lifespan.value] < lifespan_max_value / 2:
                 value = '2'
             elif x[Attr.Lifespan.value] >= lifespan_max_value / 2 and x[Attr.Lifespan.value] < lifespan_max_value - (lifespan_max_value / 4):
                 value = '3'
             elif x[Attr.Lifespan.value] >= lifespan_max_value - (lifespan_max_value / 4):
                 value = '4'
             x[Attr.Lifespan.value] = value

    """
    Método para escrever o que estiver em self.data em um CSV
    """
    def write_csv_disc(self, csv_disc):
        with open(csv_disc, 'wt') as outcsv:
            #writer = csv.DictWriter(outcsv, fieldnames = [Attr.OutcomeType.value, Attr.AnimalType.value, Attr.SexuponOutcome.value, Attr.AgeuponOutcome.value,
            #                                              Attr.Breed.value, Attr.Color.value, Attr.Lifespan.value, Attr.Adaptability.value, Attr.Size.value])
            writer = csv.DictWriter(outcsv, fieldnames = [Attr.AnimalType.value, Attr.SexuponOutcome.value, Attr.AgeuponOutcome.value,
                                                          Attr.Breed.value, Attr.Color.value, Attr.Lifespan.value, Attr.Adaptability.value, Attr.Size.value])

            writer.writeheader()
            writer.writerows(self.data)
        print('Done: write_csv_disc')

    def populate_breed_from_csv(self):
        with open('csv_discs/breed_info.csv', 'rt') as csvfile:
            dictofdata = csv.DictReader(csvfile, delimiter=',')
            self.breed_info = [{Attr.AnimalType.value: row[Attr.AnimalType.value], Attr.Breed.value: row[Attr.Breed.value], Attr.Lifespan.value: row[Attr.Lifespan.value],
                          Attr.Size.value: row[Attr.Size.value], Attr.Adaptability.value: row[Attr.Adaptability.value]} for row in dictofdata]
    print('Done: populate_breed_from_csv')

    def merge_breed_with_tuples(self):
        for animal in self.data:
            for breeddata in self.breed_info:
                if animal[Attr.Breed.value] == breeddata[Attr.Breed.value]:
                    animal[Attr.Lifespan.value] = int(breeddata[Attr.Lifespan.value]) / 30
                    animal[Attr.Size.value] = breeddata[Attr.Size.value]
                    animal[Attr.Adaptability.value] = breeddata[Attr.Adaptability.value]
        print('Done: merge_breed_with_tuples')


if __name__ == '__main__':
    csv_disc = CSVDiscretize('test.csv', 'discret_test.csv')
    csv_disc.write_csv_disc(csv_disc.new_csv)
    print('Done: final')

