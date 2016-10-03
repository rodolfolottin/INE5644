from selenium import webdriver
import os
import discretizer as disc

driver = None
data = None

_dog_breed_page = 'http://www.dogbreedslist.info/'
_cat_breed_page = 'http://www.catbreedslist.com/'

animals = [{'tipo': 'Dog'}, {'tipo': 'Cat'}]


def init_webdriver():
    global driver
    driver = webdriver.Chrome();
    driver.implicitly_wait(10)

def pre_proccess_animal(animal):
    if animal['tipo'] == 'Dog' and driver.current_url != _dog_breed_page:
        driver.get(_dog_breed_page)
    elif animal['tipo'] == 'Cat' and driver.current_url != _cat_breed_page:
        driver.get(_cat_breed_page)

def proccess_animal(animal):
    pre_proccess_animal(animal)


def run():
    print(data)
    time.sleep(20)
    init_webdriver()
    # todo get the fucking animals from csv
    for animal in animals:
        proccess_animal(animal)


if __name__ == "__main__":
    global data
    data = disc.read_csv('new_train.csv')
    run()
    driver.quit()
