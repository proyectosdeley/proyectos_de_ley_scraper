# -*- coding: utf-8 -*-
from pdl_scraper.items import PdlScraperItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class ProyectoSpider(CrawlSpider):
    name = "proyecto"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = (
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf' \
        '/PAporNumeroInverso?OpenView',
    )

    rules = (
        Rule(LinkExtractor(allow=('opendocument$',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log("this is the url: %s" % response.url)
        item = PdlScraperItem()
        item['codigo'] = ''
        item['numero_proyecto'] = ''
        item['congresistas'] = ''
        item['titulo'] = ''
        item['short_url'] = ''
        item['fecha_presentacion'] = ''
        item['expediente'] = ''
        item['pdf_url'] = ''
        item['seguimiento_page'] = ''
        item['proponente'] = ''
        item['grupo_parlamentario'] = ''
        item['iniciativas_agrupadas'] = ''
        item['nombre_comision'] = ''
        item['titulo_de_ley'] = ''
        item['numero_de_ley'] = ''

        selectors = response.xpath("//input")
        for sel in selectors:
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'CodIni_web_1':
                item['numero_proyecto'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NomCongre':
                item['congresistas'] = sel.xpath('@value').extract()[0]
            if attr_name == 'fechapre':
                item['fecha_presentacion'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesPropo':
                item['proponente'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesGrupParla':
                item['grupo_parlamentario'] = sel.xpath('@value').extract()[0]
            if attr_name == 'Titulo':
                item['titulo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'CodIniSecu':
                item['iniciativas_agrupadas'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NumLey':
                item['numero_de_ley'] = sel.xpath('@value').extract()[0]
            if attr_name == 'TitLey':
                item['titulo_de_ley'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NombreDeLaComision':
                item['nombre_comision'] = sel.xpath('@value').extract()[0]

        yield item
