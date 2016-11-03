# -*- coding: utf-8 -*-
import scrapy


class DataMiningSpider(scrapy.Spider):

    name = 'datamining'

    _base_dog_url = 'http://www.dogbreedslist.info/all-dog-breeds/'
    _base_cat_url = 'http://www.catbreedslist.com/all-cat-breeds/'

    start_urls = [
            'http://www.dogbreedslist.info/all-dog-breeds/',
            'http://www.catbreedslist.com/all-cat-breeds/'
    ]

    animal = {}

    # response.css('.list > .list-01 > .right > .right-t > p')
    """Response contém o html que foi recebido como resposta"""
    def parse(self, response):
        for animal_info in response.css('.list > .list-01 > .right > .right-t'):
            animal_info['name'] = 'bla'
            animal_info['breed_definition'] = 'bla'
        # antes de mais nada pegar o nome do animal aqui
        # e os que forem raça pura também
            yield scrapy.Request(url, callback=self.parse_animal_info)

            {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("span > small.author::text").extract_first(),
                'tags': quote.css("a.tag::text").extract()
            }

        # controla paginação
        pages_list = response.css("pages > ul > li").extract()
        for page in pages_list:
            if resp.css('a::text').extract_first() == 'Next':
                next_page = response.urljoin(resp.css('a::attr(href)').extract_first())
                yield scrapy.Request(next_page, callback=self.parse)

    # toda informação que eu desejar pegar dentro do link do animal vou pegar aqui nessa função
    def parse_animal_info(self, response):
        pass


