# -*- coding: utf-8 -*-
import scrapy

from pdl_scraper.items import UpdateFechaPresentacionItem
from pdl_scraper.models import db_connect


class UpdateFechaPresentacionSpider(scrapy.Spider):
    name = "fecha_presentacion"
    allowed_domains = ["www2.congreso.gob.pe"]

    def __init__(self, category=None, *args, **kwargs):
        super(UpdateFechaPresentacionSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.get_my_urls()

    def get_my_urls(self):
        db = db_connect()
        start_urls = []
        append = start_urls.append

        query = "select seguimiento_page from pdl_proyecto where " \
            "fecha_presentacion=''"

        res = db.query(query)
        for i in res:
            append(i['seguimiento_page'])

        return start_urls

    def parse(self, response):
        item = UpdateFechaPresentacionItem()
        item['codigo'] = ''
        item['fecha_presentacion'] = ''

        selectors = response.xpath("//input")
        for sel in selectors:
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'fechapre':
                item['fecha_presentacion'] = sel.xpath('@value').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]
        yield item
