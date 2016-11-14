import time
import sys
import settings
from csv import CSV
from attr import Attr


class DataDiscretize(object):

    def __init__(self, animal_info_csv, breed_info_csv, filetype, params, breed_params):
        self.animal_info_csv = CSV(animal_info_csv, params, True)
        self.breed_info = [for animal in CSV(breed_info_csv, breed_params, True) if animal[Attr.AnimalType] == filetype]
        self.dog_breeds = set()
        self.cat_breeds = set()
        self.data = None
        self.filetype = filetype

    """
    Método para retirar elementos que não tenham todos valores preenchidos.
    """
    def _discretize_empty_values(self):
        retirar_elementos = []
        for animal_data in self.data:
            for k, v in animal_data.items():
                if any(text in v for text in ['', ' ', 'Unknown']):
                    retirar_elementos.append(animal_data)
        self.data = [x for x in self.data if x not in retirar_elementos]
        print('Done: {func}, len of data: {l}'.format(func=discretize_empty_values, l=len(self.data)))

    """
    Método utilizado para discretizar o atributo AgeuponOutcome, que pode vir como semana, mês ou ano. Discretizado para dias.
    """
    def discretize_ageuponoutcom(self):
        for animal_data in self.data:
            if animal_data[Attr.AgeuponOutcome]:
                if 'year' in animal_data[Attr.AgeuponOutcome]:
                    day_multiplier = 365
                elif 'month' in animal_data[Attr.AgeuponOutcome]:
                    day_multiplier = 30
                elif 'week' in animal_data[Attr.AgeuponOutcome]:
                    day_multiplier = 7
                elif 'day' in animal_data[Attr.AgeuponOutcome]:
                    day_multiplier = 1
                total_dias = int(animal_data[Attr.AgeuponOutcome][0]) * day_multiplier
                animal_data[Attr.AgeuponOutcome] = total_dias / 30
        print('Done: {func}'.format(func=discretize_ageuponoutcom))

    """
    Método utilizado para discretizar e analisar raças de animais.
    """
    def discretize_breed_names(self):
        for animal_data in self.data:
            if animal_data[Attr.AnimalType] == 'Dog':
                self.dog_breeds.add(animal_data[Attr.Breed])
            elif animal_data[Attr.AnimalType] == 'Cat':
                self.cat_breeds.add(animal_data[Attr.Breed])
            else:
                print(animal_data[Attr.Breed])

            breed_animal = animal_data[Attr.Breed]
            string_match = breed_animal.find('/')
            string_match_2 = breed_animal.find(' Mix')

            if 'Black/Tan Hound Mix' in breed_animal:
                animal_data[Attr.Breed] = 'Black and Tan Coonhound'
            elif string_match != -1:
                animal_data[Attr.Breed] = breed_animal[:string_match]
                animal_data[Attr.Breed_definition] = 'Crossbreed'
            elif string_match_2 != -1:
                animal_data[Attr.Breed] = breed_animal[:string_match_2]
                animal_data[Attr.Breed_definition] = 'Crossbreed'

            animals_replace_names = {
                    'Redbone Hound': 'Redbone Coonhound',
                    'Bluetick Hound': 'Bluetick Coonhound',
                    'American Pit Bull Terrier': 'Pit Bull',
                    'Javanese': 'Japanese',
                    'St. Bernard': 'St. Bernard',
                    'Queensland Heeler': 'Australian Cattle Dog',
                    'Mastiff': 'English Mastiff'
            }

            for replace, real in animals_replace_names.items():
                if replace in animal_data[Attr.Breed]:
                    animal_data[Attr.Breed] = real

        print('Done: {}'.format(self.discretize_breed_names.__name__))

    """
    Método utilizado para analisar e discretizar o atributo Color. Existem muitas variações de nomes de cores que podem significar a mesma.
    """
    def analyze_discretize_color_names(self):
        for animal_data in self.data:
            animal_data[Attr.ColorMix] = 'No'
            match = animal_data[Attr.Color].find('/')
            if match != -1:
                animal_data[Attr.Color] = animal_data[Attr.Color][:match]
                animal_data[Attr.ColorMix] = 'Yes'
        print('Done: {}'.format(self.analyze_discretize_color_names.__name__))

    """
    Método utilizado para discretizar o atributo Size
    """
    def discretize_size_values(self):
        value = None
        for animal_data in self.data:
            try:
                if 'Small' == animal_data[Attr.Size]:
                    value = 'Small'
                elif 'Small to Medium' == animal_data[Attr.Size]:
                    value = 'Small'
                elif 'Medium' == animal_data[Attr.Size]:
                    value = 'Medium'
                elif 'Medium to Large' == animal_data[Attr.Size]:
                    value = 'Medium'
                elif 'Large' == animal_data[Attr.Size] or 'large' == animal_data[Attr.Size] or 'Largest' == animal_data[Attr.Size]:
                    value = 'Large'
                elif 'Large to Giant' == animal_data[Attr.Size]:
                    value = 'Large'
                elif 'Giant' == animal_data[Attr.Size]:
                    value = 'Giant'
                else:
                    print(animal_data[Attr.Size])
                    input()
            except Exception as e:
                print(animal_data)
            animal_data[Attr.Size] = value
        print('Done: {}'.format(self.discretize_size_values.__name__))

    """
    Método utilizado para deletar a ocorrência do texto 'stars. Lembrar que em columns tá específico para cachorros.'
    """
    def delete_stars_from_specific_columns(self):
        columns = [
               Attr.BarkingTendencies, Attr.HealthIssues, Attr.CatFriendly, Attr.ExerciseNeeds,
               Attr.Grooming, Attr.SheddingLevel, Attr.ChildFriendly, Attr.WatchdogAbility,
               Attr.DogFriendly, Attr.StrangerFriendly, Attr.Intelligence, Attr.Trainability,
               Attr.Adaptability, Attr.ApartmentFriendly, Attr.Playfulness
        ]

        for animal_data in self.data:
            for column in columns:
                animal_data[column] = animal_data[column].replace('stars', '').strip()
        print('Done: {}'.format(self.delete_stars_from_specific_columns.__name__))

    """
    @@@@@@@@ TODO
    Dividir em menos e mais? Será que é uma boa?? TODO
    """
    def discretize_puppyprice_values(self):
        for animal_data in self.data:
            string = animal_data[Attr.PuppyPrice].replace('$', '').strip()
            string = string.replace('Average', '').strip()
            string = string.replace('USD', '').strip()
        print('Done: {}'.format(self.delete_stars_from_specific_columns.__name__))

    """
    Método utilizado para analisar e discretizar sexuponoutcome e gerar sexsituationuponoutcome
    """
    def discretize_sexuponoutcome_values(self):
        situations = ['Intact', 'Spayed', 'Neutered']
        for animal_data in self.data:
            sexupon = animal_data[Attr.SexuponOutcome]
            situation = [situation for situation in situations if situation in sexupon].pop()
            animal_data[Attr.SexSituationUponOutcome] = situation
            animal_data[SexuponOutcome].replace(situation, '').strip()
         print('Done: {}'.format(self.discretize_sexuponoutcome_values.__name__))

    """
    @@@@@@@@@ TODO
    Método utilizado para gerar intervalos dos atributos AgeuponOutcome e Lifespan.
    Esses intervalos devem ser melhorados
    """
    def create_intervals(self):
         age_values = [animal[Attr.AgeuponOutcome] for animal in self.data]
         age_min_value = min(age_values)
         age_max_value = max(age_values)

         lifespan_values = [animal[Attr.Lifespan] for animal in self.data]
         lifespan_min_value = min(lifespan_values)
         lifespan_max_value = max(lifespan_values)

         for x in self.data:
             if x[Attr.AgeuponOutcome] >= age_min_value and x[Attr.AgeuponOutcome] < age_max_value / 4:
                 value = '1'
             elif x[Attr.AgeuponOutcome] >= age_max_value / 4 and x[Attr.AgeuponOutcome] < age_max_value / 2:
                 value = '2'
             elif x[Attr.AgeuponOutcome] >= age_max_value / 2 and x[Attr.AgeuponOutcome] < age_max_value - (age_max_value / 4):
                 value = '3'
             elif x[Attr.AgeuponOutcome] >= age_max_value - (age_max_value / 4):
                 value = '4'
             x[Attr.AgeuponOutcomeInterval] = value

         for x in self.data:
             if x[Attr.Lifespan] >= lifespan_min_value and x[Attr.Lifespan] < lifespan_max_value / 4:
                 value = '1'
             elif x[Attr.Lifespan] >= lifespan_max_value / 4 and x[Attr.Lifespan] < lifespan_max_value / 2:
                 value = '2'
             elif x[Attr.Lifespan] >= lifespan_max_value / 2 and x[Attr.Lifespan] < lifespan_max_value - (lifespan_max_value / 4):
                 value = '3'
             elif x[Attr.Lifespan] >= lifespan_max_value - (lifespan_max_value / 4):
                 value = '4'
             x[Attr.LifespanInterval] = value

    """
    Método utilizado para gerar o data set final
    """
    def merge_breed_with_tuples(self):
        for animal in self.data:
            for breed_data in self.breed_info:
                if animal[Attr.Breed] == breed_data[Attr.Breed]:
                    for k, v in breed_data:
                        animal[k] = v
        print('Done: merge_breed_with_tuples')


if __name__ == '__main__':
    dog_animals_params = [
            Attr.OutcomeType, Attr.OutcomeSubtype, Attr.AnimalType,
            Attr.SexuponOutcome, Attr.AgeuponOutcome, Attr.Breed, Attr.Color
    ]
    dog_breed_params = [
            Attr.PuppyPrice, Attr.BarkingTendencies, Attr.BreedName, Attr.HealthIssues,
            Attr.Hypoallergic, Attr.LitterSize, Attr.CatFriendly, Attr.ExerciseNeeds,
            Attr.Grooming, Attr.SheddingLevel, Attr.Size, Attr.ChildFriendly, Attr.WatchdogAbility,
            Attr.DogFriendly, Attr.StrangerFriendly, Attr.Intelligence, Attr.Trainability,
            Attr.Breed_definition, Attr.Adaptability, Attr.Lifespan, Attr.ApartmentFriendly,
            Attr.Playfulness
    ]
    dog_csv = DataDiscretize('train.csv', 'dog_info.csv', 'Dog', dog_animals_params, dog_breed_params)
    # chamar todas funcoes
    # retornar data
    final_csv = CSV('dog_final.csv')
    final_csv.create_new_csv('dog_final.csv', dog_data)



