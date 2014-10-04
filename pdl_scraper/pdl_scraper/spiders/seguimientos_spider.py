import scrapy

from pdl_scraper.items import SeguimientosItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = (
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Sicr/TraDocEstProc/CLProLey2011.nsf/PAporNumeroInverso/F1B568B1FDBDC0AF052578E200533CDA?opendocument',
    )

    def parse(self, response):
        for sel in response.xpath('//td[@width="112"]'):
            if sel.xpath('font/text()').extract()[0] == 'Seguimiento':
                item = SeguimientosItem()
                item['seguimientos'] = sel.xpath('following-sibling::*//text()').extract()
                item['codigo'] = "dummy"
                print(item)
                yield item

        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)