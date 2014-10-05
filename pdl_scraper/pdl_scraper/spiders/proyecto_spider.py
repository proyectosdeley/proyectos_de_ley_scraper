# -*- coding: utf-8 -*-
import short_url

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from pdl_scraper.items import PdlScraperItem


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

    def __init__(self, category=None, *args, **kwargs):
        super(ProyectoSpider, self).__init__(*args, **kwargs)
        self.legislatura = "2011"

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
        for_expediente = [
            'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf'
            '/visbusqptramdoc/',
            item['codigo'],
            '?opendocument',
        ]
        item['expediente'] = ''.join(for_expediente)
        item['seguimiento_page'] = response.url
        item['short_url'] = self.create_shorturl(item['codigo'])

        self.log("Worked on item %s." % str(item['codigo']))
        yield item


    def create_shorturl(self, codigo):
        """
        Use "legislatura" and codigo to build a short url.
        :param codigo: Code for Proyecto de ley "03774"
        :return: 4aw8ym
        """
        mystring = "%s%s" % (self.legislatura, codigo)
        url = short_url.encode_url(int(mystring))
        return url
