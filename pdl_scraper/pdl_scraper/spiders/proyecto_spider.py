import scrapy


class ProyectoSpider(scrapy.Spider):
    name = "proyecto"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = [
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf' \
        '/PAporNumeroInverso?OpenView',
    ]

    def parse(self, response):
        doc_links = self.extract_doc_links(response)

    def extract_doc_links(self, response):
        """Process frontpage of Congress and extracts links to each project."""
        our_links = []
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
                    if title is not None:
                        our_links.append({'numero_proyecto': numero_proyecto,
                                          'titulo': title,
                                          'seguimiento_page': our_link},
                                         )
        return our_links



