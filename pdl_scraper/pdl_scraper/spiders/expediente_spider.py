# -*- coding: utf-8 -*-
import scrapy

from pdl_scraper.items import ExpedienteItem
from pdl_scraper.models import db_connect
from pdl_scraper import settings


class ExpedienteSpider(scrapy.Spider):
    name = "expediente"
    allowed_domains = ["www2.congreso.gob.pe"]

    def __init__(self, category=None, *args, **kwargs):
        super(ExpedienteSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.get_my_urls()

    def get_my_urls(self):
        """Extract data from expedientes page.

        :return: List of date, URL, URL_text, project_code
        """
        db = db_connect()
        start_urls = []
        append = start_urls.append

        # get list of proyects ids from pdl_proyecto table with no events
        query = "select expediente from pdl_proyecto WHERE legislatura={}".format(settings.LEGISLATURE)
        res = db.query(query)
        for i in res:
            append(i['expediente'])
        return start_urls

    def parse(self, response):
        """We need to extract the table with links to events for this project.
        """
        events_selector = response.xpath("//table")[4]
        items = []
        this_date = ''
        pdf_url = ''
        this_text = ''
        for i in events_selector.xpath("tr"):
            item = ExpedienteItem()

            date_sel = i.xpath("td/div/font/text()").extract()
            if len(date_sel) > 0:
                this_date = date_sel[0]
                print(this_date)

            pdf_url_sel = i.xpath("td/a/@href").extract()
            if len(pdf_url_sel) > 0:
                pdf_url = pdf_url_sel[0]

            text_sel = i.xpath("td/a/b/font/text()").extract()
            if len(text_sel) > 0:
                this_text = text_sel[0]

            item['fecha'] = this_date
            item['pdf_url'] = pdf_url
            item['evento'] = this_text
            item['expediente_url'] = response.url

            if this_date != '' and pdf_url != '' and this_text != '':
                items.append(item)
        return items
