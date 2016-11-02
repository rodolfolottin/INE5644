from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from discretize.discretize import CSVDiscretizer
import time
from discretize.attr import Attr
import csv

driver = None
data = None
_dog_breed_page = 'http://www.dogbreedslist.info/'
_cat_breed_page = 'http://www.catbreedslist.com/'
visited_animals = set()
animais_nao_tratados = set()

def init_webdriver():
    global driver
    driver = webdriver.Chrome();
    driver.implicitly_wait(10)

def proccess_animal(animal):
#    if animal['AnimalType'] == 'Cat':
#        print('Animal a ser buscado: ',animal['Breed'])
#        driver.get(_dog_breed_page + 'Tags-' + animal['Breed'][0])
    if animal['AnimalType'] == 'Cat':
        print('Animal a ser buscado: ',animal['Breed'])
        driver.get(_cat_breed_page + 'Tags-' + animal['Breed'][0])
        animal_wanted = check_for_breed_in_animals_list(animal)
        if animal_wanted:
            return get_info_about_(animal_wanted, animal)
        else:
            return {'Breed': animal['Breed'], 'AnimalType': animal['AnimalType']}

def check_for_breed_in_animals_list(animal):
    try:
        animals_list = driver.find_elements_by_class_name('list')
        animal_wanted = None
        for animal_html in animals_list:
            if animal['Breed'] in animal_html.text:
                animal_wanted = animal_html
                return animal_wanted
        pages = driver.find_element_by_class_name('pages')
        lista_de_paginas = pages.find_elements_by_tag_name('li')
        if len(lista_de_paginas) == 1:
            return animal_wanted
        lista_de_paginas.pop(0)
        for pagina in lista_de_paginas:
            if pagina.find_element_by_tag_name('a').text == 'Next':
                pagina.find_element_by_tag_name('a').click()
                time.sleep(2)
                break
        return check_for_breed_in_animals_list(animal)
    except Exception as e:
        raise Exception

def get_info_about_(animal_wanted, animal):
    animal_wanted.find_element_by_xpath('div[1]/div[2]/div[1]/p/a').click()
    tbody = driver.find_element_by_tag_name('tbody')
    trs = tbody.find_elements_by_tag_name('tr')
    animal_info = {}
    animal_info['Breed'] = animal['Breed']
    animal_info['AnimalType'] = animal['AnimalType']
    for tr in trs:
        if tr.find_elements_by_tag_name('td'):
            if tr.find_elements_by_tag_name('td')[0].text == 'Life span':
                lifespan = int(tr.find_elements_by_tag_name('td')[1].text[3:5]) * 365
                animal_info['Lifespan'] = lifespan
            if tr.find_elements_by_tag_name('td')[0].text == 'Size':
                size = tr.find_elements_by_tag_name('td')[1].text
                animal_info['Size'] = size
            if tr.find_elements_by_tag_name('td')[0].text == 'Adaptability':
                adaptability = tr.find_elements_by_tag_name('td')[1].text
                animal_info['Adaptability'] = adaptability[0]
    return animal_info

def run():
    animal_info = list()
    info_animal = None
    init_webdriver()
    for animal in data:
        if animal['Breed'] not in visited_animals and animal['AnimalType'] == 'Cat':
            try:
                info_animal = proccess_animal(animal)
                print(info_animal)
                if info_animal:
                    animal_info.append(info_animal)
            except Exception as e:
                print('Animal nao tratado: ', animal['Breed'])
                animal_info.append({'Breed': animal['Breed'], 'AnimalType': animal['AnimalType']})
                animais_nao_tratados.add(animal['Breed'])
            visited_animals.add(animal['Breed'])
    print(visited_animals)
    print(animais_nao_tratados)
    return animal_info

def teste_csv(data):
    with open('pos_robot_cat.csv', 'wt') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames = [Attr.AnimalType.value, Attr.Breed.value, Attr.Lifespan.value, Attr.Adaptability.value, Attr.Size.value])
        writer.writeheader()
        writer.writerows(data)
        print('Done: write_csv_file')

if __name__ == "__main__":
    global data, animais_nao_tratados
    disc = CSVDiscretizer('teste_1.csv', 'pos_robot_cat.csv', False)
    data = disc.populate_data_from_csv('csv_files/teste_1.csv', True)
    animals = run()
    teste_csv(animals)
    driver.quit()

