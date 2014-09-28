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
        selectors = response.xpath("//input")
        codigo, numero_proyecto, congresistas = '', '', ''

        for sel in selectors:
            attr_name = sel.xpath('@name').extract()[0]

            if attr_name == 'CodIni':
                codigo = sel.xpath('@value').extract()[0]
                self.log("INFO: this is codigo %s" % codigo)
            if attr_name == 'CodIni_web_1':
                numero_proyecto = sel.xpath('@value').extract()[0]
                self.log("INFO: this is numero_proyecto %s" % numero_proyecto)
            if attr_name == 'NomCongre':
                congresistas = sel.xpath('@value').extract()[0]
                self.log("INFO: this is congresistas %s" % congresistas)

        if codigo != '' and numero_proyecto != '' and congresistas != '':
            item = PdlScraperItem()
            item['codigo'] = codigo
            item['numero_proyecto'] = numero_proyecto
            item['congresistas'] = congresistas
            yield item
