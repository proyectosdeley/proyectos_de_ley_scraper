# -*- coding: utf-8 -*-
import scrapy


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
        query = "select expediente, pdf_url from pdl_proyecto"
        res = db.query(query)
        for i in res:
            if i['pdf_url'] is None or i['pdf_url'].strip() == '':
                append(i['expediente'])
                log.msg('Appending %s to start_urls.' % str(i['expediente']))

        return start_urls

    def parse(self, response):
        """We need to extract the table with links to events for this project.
        """
        selectors = response.xpath("//table")
        events_selector = selectors[2]
        pass

