# -*- coding: utf-8 -*-
import scrapy
from pdl_scraper.models import db_connect
from pdl_scraper.items import IniciativaItem
from pdl_scraper import settings


class IniciativaSpider(scrapy.Spider):
    name = 'iniciativa'
    allowed_domains = ["www2.congreso.gob.pe"]

    def __init__(self, category=None, *args, **kwargs):
        super(IniciativaSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.get_my_urls()

    def get_my_urls(self):
        db = db_connect()
        start_urls = []
        append = start_urls.append

        query = "select codigo, iniciativas_agrupadas, seguimiento_page " \
                "from pdl_proyecto WHERE legislatura={} order by time_edited".format(settings.LEGISLATURE)
        res = db.query(query)

        for i in res:
            iniciativas = i['iniciativas_agrupadas']
            if type(iniciativas) == list:
                if len(iniciativas) < 1:
                    if i['seguimiento_page'] != '':
                        # this field is empty, scrape it!
                        append(i['seguimiento_page'])

            elif iniciativas is None:
                if i['seguimiento_page'] != '':
                    append(i['seguimiento_page'])

            elif iniciativas.strip() == '':
                if i['seguimiento_page'] != '':
                    append(i['seguimiento_page'])

        return start_urls

    def parse(self, response):
        item = IniciativaItem()
        for sel in response.xpath("//input"):
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]

            if attr_name == 'CodIniSecu':
                item['iniciativas_agrupadas'] = sel.xpath('@value').extract()[0]
        yield item
