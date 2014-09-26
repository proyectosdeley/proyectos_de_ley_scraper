import scrapy


class ProyectoSpider(scrapy.Spider):
    name = "proyecto"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = [
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf' \
        '/PAporNumeroInverso?OpenView',
    ]

    def parse(self, response):
        for sel in response.xpath("//a"):
            if re.search("[0-9]{5}/[0-9]{4}", sel.extract()):
                numero_proyecto = sel.xpath('text()').extract()
                href = sel.xpath("//a/@href").extract()
                title = sel.xpath("//a/@title").extract()

                if href.endswith("ocument"):
                    for_link = [
                        "http://www2.congreso.gob.pe",
                        "/Sicr/TraDocEstProc/CLProLey2011.nsf/",
                        href,
                    ]
                    our_link = ''.join(for_link)


