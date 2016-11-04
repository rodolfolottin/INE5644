# -*- coding: utf-8 -*-
import scrapy


class DataMiningSpider(scrapy.Spider):

    name = 'datamining'

    _base_dog_url = 'http://www.dogbreedslist.info/all-dog-breeds/'
    _base_cat_url = 'http://www.catbreedslist.com/all-cat-breeds/'

    start_urls = (
            'http://www.dogbreedslist.info/all-dog-breeds/',
            # 'http://www.catbreedslist.com/all-cat-breeds/'
    )


    """Response contém o html que foi recebido como resposta"""
    def parse(self, response):
        for each_list_animal in response.css('.list > .list-01 > .right > .right-t'):

            animal_info = {}
            animal_info['Name'] = each_list_animal.css('p > a::text').extract_first()
            animal_info['Breed_definition'] = each_list_animal.css('span::text').extract_first()

            animal_url = each_list_animal.css('p > a::attr(href)').extract_first()
            yield scrapy.Request(animal_url, callback=self.parse_animal_info, meta={'animal_info': animal_info})

        # controla paginação
        pages_list = response.css(".pages > ul > li")
        for page in pages_list:
            if page.css('a'):
                if page.css('a::text').extract_first() == 'Next':
                    next_page = response.urljoin(page.css('a::attr(href)').extract_first())
                    yield scrapy.Request(next_page, callback=self.parse)

    def parse_animal_info(self, response):
        # rascunho
        # animal_info['Size'] = response.css('.content > table > tbody > tr > td').extract_first()
        animal_info = response.meta.get('animal_info')
        animal_info['Size'] = 'Teste'
        yield animal_info


