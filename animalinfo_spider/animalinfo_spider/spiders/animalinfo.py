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
        animal_info = response.meta.get('animal_info')

        trs_list = response.css('.table-01 > tbody > tr > td').extract()
        self._parse_trs_list(trs_list)

        animal_info['Size'] = 'Teste'
        yield animal_info

    def _parse_by_xpath(self, response):
        # best way to remove first element from a list
        'Adaptability': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[19]/td[2]/span/text()').extract_first()
        'Apartment Friendly': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[20]/td[2]/span/text()').extract_first()
        'Barking Tendencies': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[21]/td[2]/span[1]/text()').extract_first()
        'Cat Friendly': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[22]/td[2]/span/text()').extract_first()
        'Child Friendly': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[23]/td[2]/span[1]/text()').extract_first()
        'Dog Friendly': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[24]/td[2]/span/text()').extract_first()
        'Exercise Needs': response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[25]/td[2]/span/text()').extract_first()

