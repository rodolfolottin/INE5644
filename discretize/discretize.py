import time
import sys
import settings
from data_csv import CSV
from attr import Attr


class DataDiscretize(object):

    def __init__(self, animal_info_csv, breed_info_csv, filetype, params, breed_params, should_exec=False):
        self.animal_info = [animal_data for animal_data in CSV(animal_info_csv, params, True).csv_data if animal_data[Attr.AnimalType.value] == filetype]
        self.breed_info = [animal for animal in CSV(breed_info_csv, breed_params, True).csv_data]
        self.dog_breeds = set()
        self.cat_breeds = set()
        self.filetype = filetype
        if should_exec:
            self._discretize_empty_values()
            self.discretize_breed_names()
            self.discretize_ageuponoutcom()
            self.merge_breed_with_tuples()
            self.discretize_size_values()
            self.discretize_littersize_values()
            self.discretize_puppyprice_values()
            self.discretize_sexuponoutcome_values()
            self.analyze_discretize_color_names()
            self.delete_stars_from_specific_columns()

    """
    Método para retirar elementos que não tenham todos valores preenchidos.
    """
    def _discretize_empty_values(self):
        retirar_elementos = []
        for animal_data in self.animal_info:
            for k, v in animal_data.items():
                if v == '' or v == 'Unknown' or v == ' ' or 'Unknown' in v:
                    retirar_elementos.append(animal_data)
        antigo_len = len(self.animal_info)
        self.animal_info = [x for x in self.animal_info if x not in retirar_elementos]
        print('Done: {func}, len of data: {l}, after: {a}'.format(func=self._discretize_empty_values.__name__, a=len(self.animal_info), l=antigo_len))

    """
    Método utilizado para discretizar o atributo AgeuponOutcome, que pode vir como semana, mês ou ano. Discretizado para dias.
    """
    def discretize_ageuponoutcom(self):
        for animal_data in self.animal_info:
            if animal_data[Attr.AgeuponOutcome.value]:
                if 'year' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 365
                elif 'month' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 30
                elif 'week' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 7
                elif 'day' in animal_data[Attr.AgeuponOutcome.value]:
                    day_multiplier = 1
                total_dias = int(animal_data[Attr.AgeuponOutcome.value][0]) * day_multiplier
                animal_data[Attr.AgeuponOutcome.value] = total_dias
        print('Done: {func}'.format(func=self.discretize_ageuponoutcom.__name__))

    """
    Método utilizado para discretizar e analisar raças de animais.
    """
    def discretize_breed_names(self):
        for animal_data in self.animal_info:
            if animal_data[Attr.AnimalType.value] == 'Dog':
                self.dog_breeds.add(animal_data[Attr.Breed.value])
            elif animal_data[Attr.AnimalType.value] == 'Cat':
                self.cat_breeds.add(animal_data[Attr.Breed.value])
            else:
                print(animal_data[Attr.Breed.value])

            breed_animal = animal_data[Attr.Breed.value]
            string_match = breed_animal.find('/')
            string_match_2 = breed_animal.find(' Mix')

            if 'Black/Tan Hound Mix' in breed_animal:
                animal_data[Attr.Breed.value] = 'Black and Tan Coonhound'
            elif string_match != -1:
                animal_data[Attr.Breed.value] = breed_animal[:string_match]
                animal_data[Attr.Breed_definition.value] = 'Crossbreed'
            elif string_match_2 != -1:
                animal_data[Attr.Breed.value] = breed_animal[:string_match_2]
                animal_data[Attr.Breed_definition.value] = 'Crossbreed'

            animals_replace_names = {
                    'Redbone Hound': 'Redbone Coonhound',
                    'Bluetick Hound': 'Bluetick Coonhound',
                    'American Pit Bull Terrier': 'Pit Bull',
                    'Javanese': 'Japanese',
                    'St. Bernard': 'St. Bernard',
                    'Queensland Heeler': 'Australian Cattle Dog',
                    'Mastiff': 'English Mastiff',
                    'Chihuahua Shorthair': 'Chihuahua',
                    'Dachshund Longhair': 'Dachshund',
                    'Dachshund Wirehair': 'Dachshund',
                    'English Pointer': 'Pointer',
                    'Chihuahua Longhair': 'Chihuahua',
                    'English Bulldog': 'Bulldog',
                    'Old English Bulldog': 'Bulldog',
                    'Doberman Pinsch': 'Doberman Pinscher',
                    'Cocker Spaniel': 'American Cocker Spaniel',
                    'Mexican Hairless': 'Xoloitzcuintli',
                    'West Highland': 'West Highland White Terrier',
                    'Staffordshire': 'American Staffordshire Terrier',
                    'Brittany': 'French Brittany',
                    'Flat Coat Retriever': 'Flat-Coated Retriever',
                    'Chesa Bay Retr': 'Chesapeake Bay Retriever',
                    'Rhod Ridgeback': 'Rhodesian Ridgeback',
                    'Collie Rough': 'Collie',
                    'Bruss Griffon': 'Brussels Griffon',
                    'Chinese Sharpei': 'Shar-Pei',
                    'Miniature Poodle': 'Toy Poodle',
                    'German Shorthair Pointer': 'German Shorthaired Pointer',
                    'Boykin Span': 'Boykin Spaniel',
                    'Schnauzer Giant': 'Giant Schnauzer',
                    'American Eskimo': 'American Eskimo Dog',
                    'Wire Hair Fox Terrier': 'Wire Fox Terrier',
                    'Cavalier Span': 'Cavalier King Charles Spaniel',
                    'Standard Poodle': 'Poodle',
                    'Podengo Pequeno': 'Portuguese Podengo Pequeno',
                    'Pbgv': 'Petit Basset Griffon Vendeen',
                    'Patterdale Terr': 'Patterdale Terrier',
                    'English Coonhound': 'American English Coonhound',
                    'Jindo': 'Korean Jindo Dog',
                    'Bedlington Terr': 'Bedlington Terrier',
                    'Entlebucher': 'Entlebucher Mountain Dog',
                    'Glen of Imaal': 'Glen of Imaal Terrier',
                    'Glen Of Imaal': 'Glen of Imaal Terrier',
                    'Dogue De Bordeaux': 'Dogue de Bordeaux',
                    'Bedlington Terr': 'Bedlington Terrier',
                    'Black': 'Black and Tan Coonhound',
                    'Port Water Dog': 'Portuguese Water Dog',
                    'Sealyham Terr': 'Sealyham Terrier',
                    'Bull Terrier Miniature': 'Miniature Bull Terrier'
            }

            for replace, real in animals_replace_names.items():
                if replace in animal_data[Attr.Breed.value]:
                    animal_data[Attr.Breed.value] = real

        print('Done: {}'.format(self.discretize_breed_names.__name__))

    """
    Método utilizado para analisar e discretizar o atributo Color. Existem muitas variações de nomes de cores que podem significar a mesma.
    """
    def analyze_discretize_color_names(self):
        for animal_data in self.animal_info:
            animal_data[Attr.ColorMix.value] = 'No'
            match = animal_data[Attr.Color.value].find('/')
            if match != -1:
                animal_data[Attr.Color.value] = animal_data[Attr.Color.value][:match]
                animal_data[Attr.ColorMix.value] = 'Yes'
        print('Done: {}'.format(self.analyze_discretize_color_names.__name__))

    """
    Método utilizado para discretizar o atributo Size
    """
    def discretize_size_values(self):
        value = None
        for animal_data in self.animal_info:
            try:
                if animal_data[Attr.Size.value] in ['Small', 'small']:
                    value = 1 # 'Small'
                elif animal_data[Attr.Size.value] in ['Small to Medium']:
                    value = 2 #'Small'
                elif animal_data[Attr.Size.value] in ['Medium', 'medium', 'Medium dog breeds']:
                    value = 3 #'Medium'
                elif animal_data[Attr.Size.value] in ['Medium to Large']:
                    value = 4 #'Medium'
                elif animal_data[Attr.Size.value] in ['large', 'Largest', 'Large sized', 'Large']:
                    value = 5 #'Large'
                elif animal_data[Attr.Size.value] in ['Large to Giant']:
                    value = 6 #'Large'
                elif animal_data[Attr.Size.value] in ['Giant']:
                    value = 7 #'Giant'
                else:
                    print(animal_data[Attr.Size.value])
                    input()
            except Exception as e:
                print(animal_data)
            animal_data[Attr.Size.value] = value
        print('Done: {}'.format(self.discretize_size_values.__name__))

    """
    Método utilizado para deletar a ocorrência do texto 'stars. Lembrar que em columns tá específico para cachorros.'
    """
    def delete_stars_from_specific_columns(self):
        # dog columns
        columns = [
               Attr.BarkingTendencies, Attr.HealthIssues, Attr.CatFriendly, Attr.ExerciseNeeds,
               Attr.Grooming, Attr.SheddingLevel, Attr.ChildFriendly, Attr.WatchdogAbility,
               Attr.DogFriendly, Attr.StrangerFriendly, Attr.Intelligence, Attr.Trainability,
               Attr.Adaptability, Attr.ApartmentFriendly, Attr.Playfulness
        ]
        if self.filetype == 'Cat':
            columns = [
                Attr.Adaptability, Attr.AffectionLevel, Attr.Vocalization,
                Attr.ChildFriendly, Attr.StrangerFriendly, Attr.DogFriendly,
                Attr.SocialNeeds, Attr.EnergyLevel, Attr.HealthIssues,
                Attr.Intelligence, Attr.Grooming, Attr.Shedding
            ]
        for animal_data in self.animal_info:
            for column in columns:
                animal_data[column.value] = animal_data[column.value].replace('stars', '').strip()
        print('Done: {}'.format(self.delete_stars_from_specific_columns.__name__))

    """
    Método utilizado para alterar o valor de PuppyPrice para a média dos valores que aparecem
    """
    def discretize_puppyprice_values(self):
        eliminate_chars = ['Average', 'USD', '$']
        for animal_data in self.animal_info:
            string = animal_data[Attr.PuppyPrice.value]
            for char in eliminate_chars:
                string = string.replace(char, '').strip()
            average = 0
            values_list = string.split('-')
            for value in values_list:
                average += int(value.strip())
            animal_data[Attr.PuppyPrice.value] = int(round(average / len(values_list)))
        print('Done: {}'.format(self.delete_stars_from_specific_columns.__name__))

    """
    Método utilizado para analisar e discretizar sexuponoutcome e gerar sexsituationuponoutcome
    """
    def discretize_sexuponoutcome_values(self):
        situations = ['Intact', 'Spayed', 'Neutered']
        for animal_data in self.animal_info:
            sexupon = animal_data[Attr.SexuponOutcome.value]
            situation = [situation for situation in situations if situation in sexupon].pop()
            animal_data[Attr.SexSituationUponOutcome.value] = situation
            animal_data[Attr.SexuponOutcome.value] = sexupon.replace(situation, '').strip()
        print('Done: {}'.format(self.discretize_sexuponoutcome_values.__name__))

    """
    Método utilizado para discretizar litter size
    """
    def discretize_littersize_values(self):
        for animal_data in self.animal_info:
            string = animal_data[Attr.LitterSize.value]
            if string.find('average') != -1:
                animal_data[Attr.LitterSize.value] = int(string[-1])
                continue
            string = string.replace('puppies', '').strip()
            string = string.replace('puppies', '').strip()
            values_list = string.split('-')
            average = 0
            for value in values_list:
                average += int(value.strip())
            animal_data[Attr.LitterSize.value] = int(round(average / 2))
        print('Done: {}'.format(self.discretize_littersize_values.__name__))

    """
    @@@@@@@@@ TODO
    Método utilizado para gerar intervalos dos atributos AgeuponOutcome e Lifespan.
    Esses intervalos devem ser melhorados
    """
    def create_intervals(self):
         age_values = [animal[Attr.AgeuponOutcome.value] for animal in self.animal_info]
         age_min_value = min(age_values)
         age_max_value = max(age_values)

         lifespan_values = [animal[Attr.Lifespan.value] for animal in self.animal_info]
         lifespan_min_value = min(lifespan_values)
         lifespan_max_value = max(lifespan_values)

         for x in self.animal_info:
             if x[Attr.AgeuponOutcome.value] >= age_min_value and x[Attr.AgeuponOutcome.value] < age_max_value / 4:
                 value = '1'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value / 4 and x[Attr.AgeuponOutcome.value] < age_max_value / 2:
                 value = '2'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value / 2 and x[Attr.AgeuponOutcome.value] < age_max_value - (age_max_value / 4):
                 value = '3'
             elif x[Attr.AgeuponOutcome.value] >= age_max_value - (age_max_value / 4):
                 value = '4'
             x[Attr.AgeuponOutcomeInterval.value] = value

         for x in self.animal_info:
             if x[Attr.Lifespan.value] >= lifespan_min_value and x[Attr.Lifespan.value] < lifespan_max_value / 4:
                 value = '1'
             elif x[Attr.Lifespan.value] >= lifespan_max_value / 4 and x[Attr.Lifespan.value] < lifespan_max_value / 2:
                 value = '2'
             elif x[Attr.Lifespan.value] >= lifespan_max_value / 2 and x[Attr.Lifespan.value] < lifespan_max_value - (lifespan_max_value / 4):
                 value = '3'
             elif x[Attr.Lifespan.value] >= lifespan_max_value - (lifespan_max_value / 4):
                 value = '4'
             x[Attr.LifespanInterval.value] = value

    """
    Método utilizado para gerar o data set final
    """
    def merge_breed_with_tuples(self):
        for animal in self.animal_info:
            for breed_data in self.breed_info:
                if animal[Attr.Breed.value] == breed_data[Attr.Breed.value]:
                    for k, v in breed_data.items():
                        animal[k] = v
        print('Done: merge_breed_with_tuples')


if __name__ == '__main__':
    dog_animals_params = [
            Attr.OutcomeType, Attr.AnimalType, Attr.SexuponOutcome,
            Attr.AgeuponOutcome, Attr.Breed, Attr.Color
    ]
    dog_breed_params = [
            Attr.PuppyPrice, Attr.BarkingTendencies, Attr.Breed, Attr.HealthIssues,
            Attr.Hypoallergenic, Attr.LitterSize, Attr.CatFriendly, Attr.ExerciseNeeds,
            Attr.Grooming, Attr.SheddingLevel, Attr.Size, Attr.ChildFriendly, Attr.WatchdogAbility,
            Attr.DogFriendly, Attr.StrangerFriendly, Attr.Intelligence, Attr.Trainability,
            Attr.Breed_definition, Attr.Adaptability, Attr.Lifespan, Attr.ApartmentFriendly,
            Attr.Playfulness
    ]
    cat_animals_params = [
                Attr.Adaptability, Attr.AffectionLevel, Attr.Vocalization, Attr.Size,
                Attr.ChildFriendly, Attr.Lifespan, Attr.StrangerFriendly, Attr.DogFriendly,
                Attr.MaxPounds, Attr.SocialNeeds, Attr.Breed, Attr.EnergyLevel, Attr.HealthIssues,
                Attr.Hypoallergenic, Attr.Intelligence, Attr.KittenPrice, Attr.Grooming, Attr.LapCat,
                Attr.Shedding
    ]
    dog_csv = DataDiscretize('train.csv', 'dog_info.csv', 'Dog', dog_animals_params, dog_breed_params, True)
    final_csv = CSV('dog_final.csv')
    final_csv.create_new_csv('dog_final.csv', dog_csv.animal_info)



