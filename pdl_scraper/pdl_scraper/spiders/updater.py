# -*- coding: utf-8 -*-
import scrapy

from pdl_scraper.items import UpdaterItem
from pdl_scraper.models import db_connect


class UpdaterSpider(scrapy.Spider):
    """Updates some fields that were added later."""
    name = "updater"
    allowed_domains = ["www2.congreso.gob.pe"]

    def __init__(self, category=None, *args, **kwargs):
        super(UpdaterSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.get_my_urls()

    def parse(self, response):
        item = UpdaterItem()
        item['codigo'] = ''
        item['proponente'] = ''
        item['grupo_parlamentario'] = ''
        item['nombre_comision'] = ''
        item['titulo_de_ley'] = ''
        item['numero_de_ley'] = ''

        selectors = response.xpath("//input")
        for sel in selectors:
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesPropo':
                item['proponente'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesGrupParla':
                item['grupo_parlamentario'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NombreDeLaComision':
                item['nombre_comision'] = sel.xpath('@value').extract()[0]
            if attr_name == 'TitLey':
                item['titulo_de_ley'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NumLey':
                item['numero_de_ley'] = sel.xpath('@value').extract()[0]
        yield item

    def get_my_urls(self):
        db = db_connect()
        start_urls = []
        append = start_urls.append

        query = "select seguimiento_page from pdl_proyecto where " \
            "proponente = '' or " \
            "grupo_parlamentario = '' or " \
            "nombre_comision = '' or " \
            "titulo_de_ley = '' or " \
            "numero_de_ley = '' or " \
            "proponente is null or " \
            "grupo_parlamentario is null or "  \
            "nombre_comision is null or " \
            "titulo_de_ley is null or " \
            "numero_de_ley is null"

        res = db.query(query)
        for i in res:
            append(i['seguimiento_page'])

        return start_urls