import scrapy
from scrapy import log

from pdl_scraper.items import SeguimientosItem
from pdl_scraper.models import db_connect
from pdl_scraper import settings


class SeguimientoSpider(scrapy.Spider):
    name = "seguimientos"
    allowed_domains = ["www2.congreso.gob.pe"]

    def __init__(self, category=None, *args, **kwargs):
        super(SeguimientoSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.get_my_urls()

    def parse(self, response):
        item = SeguimientosItem()
        for sel in response.xpath("//input"):
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]

        for sel in response.xpath('//td[@width="112"]'):
            if sel.xpath('font/text()').extract()[0] == 'Seguimiento':
                item['seguimientos'] = sel.xpath('following-sibling::*//text()').extract()

        yield item

    def get_my_urls(self):
        """
        Find those proyectos with no seguimientos in our database or those
        that need to be updates.
        :return: set of URLs
        """
        db = db_connect()
        start_urls = []
        append = start_urls.append

        # get list of proyects ids from pdl_proyecto table with no events
        query = "select seguimiento_page, pdl_proyecto.id, codigo, evento " \
                "from pdl_proyecto LEFT OUTER JOIN pdl_seguimientos ON " \
                "(pdl_proyecto.id = pdl_seguimientos.proyecto_id) WHERE " \
                "pdl_proyecto.legislatura={}".format(settings.LEGISLATURE)
        res = db.query(query)
        for i in res:
            if i['evento'] is None:
                append(i['seguimiento_page'])

        # get list of proyectos ids from pdl_proyecto table with events but
        # are not law yet

        # first, get those that are law
        these_proyecto_ids_are_law = []
        append = these_proyecto_ids_are_law.append
        # use a SQLalchemy expression
        table = db['pdl_seguimientos'].table
        query = table.select(table.c.evento.like('%Promulgado%') |
                             table.c.evento.like('%Publicado%'))
        res = db.query(query)
        for i in res:
            if i['proyecto_id'] not in these_proyecto_ids_are_law:
                append(i['proyecto_id'])

        # now get those that have events but are not law already
        these_proyecto_ids_are_not_law = []
        append = these_proyecto_ids_are_not_law.append
        query = "select distinct proyecto_id from pdl_seguimientos " \
                "LEFT OUTER JOIN pdl_proyecto ON " \
                "(pdl_proyecto.id = pdl_seguimientos.proyecto_id) where "\
                "pdl_proyecto.legislatura = {}".format(settings.LEGISLATURE)
        res = db.query(query)
        for i in res:
            if i['proyecto_id'] not in these_proyecto_ids_are_law and \
                    i['proyecto_id'] not in these_proyecto_ids_are_not_law:
                log.msg("Appending %s" % str(i['proyecto_id']))
                append(i['proyecto_id'])

        # get proyecto codes from proyecto ids and add to URL list
        table = db['pdl_proyecto']
        for i in these_proyecto_ids_are_not_law:
            res = table.find_one(id=i)
            if res is not None:
                if res['seguimiento_page'] not in start_urls:
                    start_urls.append(res['seguimiento_page'])

        return start_urls
