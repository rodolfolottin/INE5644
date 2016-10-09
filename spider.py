from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import discretizer as disc
import time
from attr import Attr

driver = None
data = None
_dog_breed_page = 'http://www.dogbreedslist.info/'
_cat_breed_page = 'http://www.catbreedslist.com/'
animals_info = {}
visited_animals = set()


data = [{'Breed': 'Labrador Retriever', 'AnimalType': 'Dog'} , {'Breed': 'Pomeranian', 'AnimalType': 'Dog'}]


def init_webdriver():
    global driver
    driver = webdriver.Chrome();
    driver.implicitly_wait(10)

def proccess_animal(animal):
    if animal['AnimalType'] == 'Dog':
        driver.get(_dog_breed_page + 'Tags-' + animal['Breed'][0])
    elif animal['AnimalType'] == 'Cat':
        driver.get(_cat_breed_page + 'Tags-' + animal['Breed'][0])
    animal_wanted = check_for_breed_in_animals_list(animal)
    if animal_wanted:
        get_info_about_(animal_wanted, animal)

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
        lista_de_paginas.pop(0)
        for pagina in lista_de_paginas:
            if pagina.find_element_by_tag_name('a').text == 'Next':
                pagina.find_element_by_tag_name('a').click()
                time.sleep(2)
                break
        return check_for_breed_in_animals_list(animal)
    except Exception as e:
        print(e)
        input()

def get_info_about_(animal_wanted, animal):
    print('get_info_about')
    animal_wanted.find_element_by_xpath('div[1]/div[2]/div[1]/p/a').click()
    tbody = driver.find_element_by_tag_name('tbody')
    trs = tbody.find_elements_by_tag_name('tr')
    animals_info[animal['Breed']] = {}
    print(animals_info)
    for tr in trs:
        if tr.find_elements_by_tag_name('td'):
            if tr.find_elements_by_tag_name('td')[0].text == 'Life span':
                lifespan = int(tr.find_elements_by_tag_name('td')[1].text[3:5]) * 365
                animals_info[animal['Breed']]['Lifespan'] = lifespan
            if tr.find_elements_by_tag_name('td')[0].text == 'Size':
                size = tr.find_elements_by_tag_name('td')[1].text
                animals_info[animal['Breed']]['size'] = size
            if tr.find_elements_by_tag_name('td')[0].text == 'Adaptability':
                adaptability = tr.find_elements_by_tag_name('td')[1].text
                animals_info[animal['Breed']]['adaptability'] = adaptability[0]
    print(animals_info)
    if not animals_info[animal['Breed']]: del animals_info[animal['Breed']]

def run():
    init_webdriver()
    # todo get the fucking animals from csv
    for animal in data:
        if animal['Breed'] not in visited_animals:
            try:
                proccess_animal(animal)
            except Exception as e:
                print(e)
            visited_animals.add(animal['Breed'])

if __name__ == "__main__":
    global data
    #data = disc.read_csv('new_train.csv')
    run()
    driver.quit()

