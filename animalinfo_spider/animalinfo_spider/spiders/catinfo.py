# -*- coding: utf-8 -*-
import scrapy


class CatMiningSpider(scrapy.Spider):

    name = 'catmining'

    cat_names = ['Domestic Shorthair', 'Angora', 'Russian Blue', 'Domestic Longhair', 'Siamese', 'Domestic Medium Hair', 'Manx',
                    'Exotic Shorthair', 'Devon Rex', 'Snowshoe', 'Maine Coon', 'Burmese', 'Bengal', 'American Shorthair', 'Himalayan'
                    'Ragdoll', 'Bombay', 'Persian', 'Cornish Rex', 'Balinese', 'Japanese', 'British Shorthair', 'Japanese Bobtail',
                    'Pixiebob Shorthair', 'Tonkinese', 'Sphynx', 'Ocicat', 'Abyssinian', 'Munchkin Longhair', 'Turkish Van',
                    'Norwegian Forest Cat', 'Cymric', 'Havana Brown'
            ]

    _base_cat_url = 'http://www.catbreedslist.com/all-cat-breeds/'

    start_urls = [
            'http://www.catbreedslist.com/all-cat-breeds/'
    ]


    """Response contém o html que foi recebido como resposta"""
    def parse(self, response):
        for each_list_animal in response.css('.main > .main-r > .list'):

            animal_info = {}
            animal_info['Name'] = each_list_animal.css('.list-01 > .right > .right-t > p > a::text').extract_first()
            if animal_info['Name'] not in self.cat_names:
                continue
            animal_info['Hypoallergenic'] = each_list_animal.css('div.list-01 > div.right > div.right-c > div.hyp > p::text').extract_first()
            animal_info['Max Pounds'] = each_list_animal.css('div.list-01 > div.right > div.right-c > div.int > p::text').extract_first()

            animal_url = each_list_animal.css('div.list-01 > div.right > div.right-t > p > a::attr(href)').extract_first()
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
        # aqui fazer verificacoes de que tipo de DOM estamos falando
        self._build_info_by_xpath_1(response, animal_info)
        yield animal_info

    def _build_info_by_xpath_1(self, response, animal_info):
        try:
            animal_info['Lap Cat'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[9]/td[2]/text()').extract_first()
            animal_info['Size'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[7]/td[2]/text()').extract_first()
            animal_info['Kitten Price'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[14]/td[2]/text()').extract_first()
            animal_info['Lifespan'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[10]/td[2]/text()').extract_first()
            animal_info['Adaptability'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[17]/td[2]/span/text()').extract_first()
            animal_info['Affection Level'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[18]/td[2]/span/text()').extract_first()
            animal_info['Child Friendly'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[19]/td[2]/span[1]/text()').extract_first()
            animal_info['Dog Friendly'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[20]/td[2]/span/text()').extract_first()
            animal_info['Energy Level'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[21]/td[2]/span/text()').extract_first()
            animal_info['Grooming'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[22]/td[2]/span[1]/text()').extract_first()
            animal_info['Health Issues'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[23]/td[2]/span[1]/text()').extract_first()
            animal_info['Intelligence'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[24]/td[2]/span/text()').extract_first()
            animal_info['Shedding'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[25]/td[2]/span[1]/text()').extract_first()
            animal_info['Social Needs'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[26]/td[2]/span/text()').extract_first()
            animal_info['Stranger Friendly'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[27]/td[2]/span/text()').extract_first()
            animal_info['Vocalization'] = response.xpath('/html/body/div[2]/div[2]/div[4]/table[1]/tbody/tr[28]/td[2]/span[1]/text()').extract_first()
        except Exception as e:
            print(e)
            input()

