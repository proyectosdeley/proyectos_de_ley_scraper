import scrapy

from pdl_scraper.items import SeguimientosItem


class SeguimientoSpider(scrapy.Spider):
    name = "seguimientos"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = (
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Sicr/TraDocEstProc/CLProLey2011.nsf/PAporNumeroInverso/F1B568B1FDBDC0AF052578E200533CDA?opendocument',
    )

    def parse(self, response):
        for sel in response.xpath('//td[@width="112"]'):
            if sel.xpath('font/text()').extract()[0] == 'Seguimiento':
                item = SeguimientosItem()
                item['seguimientos'] = sel.xpath('following-sibling::*//text()').extract()
                #self.log('item seguimientos2 %s' % item['seguimientos2'])
                item['codigo'] = u"00001"
                #self.log('item codigo2 %s' % item['codigo2'])

                yield item
