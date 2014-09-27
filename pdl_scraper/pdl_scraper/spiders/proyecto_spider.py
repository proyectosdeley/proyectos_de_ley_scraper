from __future__ import absolute_import
import re

import sqlalchemy
import scrapy
from pdl_scraper.items import PdlScraperItem
from pdl_scraper.models import Proyecto, db_connect, create_proyecto_table
from sqlalchemy.orm import sessionmaker


class ProyectoSpider(scrapy.Spider):
    name = "proyecto"
    allowed_domains = ["www2.congreso.gob.pe"]
    start_urls = [
        'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf' \
        '/PAporNumeroInverso?OpenView',
    ]

    def __init__(self):
        db = db_connect()
        self.table = db['pdl_proyecto']

    def parse(self, response):
        items = []
        append = items.append
        selectors = response.xpath("//a")
        for sel in selectors:
            href = sel.xpath("@href").extract()
            if href[0].endswith('opendocument'):
                for_link = [
                    "http://www2.congreso.gob.pe",
                    "/Sicr/TraDocEstProc/CLProLey2011.nsf/",
                    href[0],
                ]
                our_link = ''.join(for_link)
                item = PdlScraperItem()
                item['numero_proyecto'] = sel.xpath('text()').extract()[0]
                item['seguimiento_page'] = our_link
                item['titulo'] = sel.xpath("@title").extract()[0]

                if self.is_in_db(item) is False:
                    # continue scraping
                    append(item)
        return items

        # doc_links = self.extract_doc_links(response)
        # return doc_links
        """
        for obj in doc_links:
            print("Working on %s:" % obj['numero_proyecto'])
            obj = self.gather_all_metadata(obj)
            if obj != "already in database":
                # save
                self.save_project(obj)
                self.save_slug(obj)
                print("Saved %s" % obj['codigo'])
            else:
                print("\t" + obj)

            print("Working on seguimientos")
            seguimientos_soup = self.get(obj['seguimiento_page'])
            seguimientos = self.get_seguimientos(seguimientos_soup)
            if seguimientos != '':
                self.save_seguimientos(seguimientos, obj['codigo'])

            if 'test' in options and options['test'] is True:
                break
        """

    def is_in_db(self, item):
        res = self.table.find_one(numero_proyecto=item['numero_proyecto'])
        if res is None:
            return False
        else:
            return True



    def gather_all_metadata(self, obj):
        """
        Uses several functions to pull all metadata for a certain proyecto.
        :param obj: dict {'numero_proyecto', 'titulo', 'seguimiento_page'}
        :return: dict containing all needed metadata.
        """
        obj = self.extract_metadata(obj)
        if obj != "already in database":
            obj['short_url'] = self.create_shorturl(obj['codigo'])
            obj['fecha_presentacion'] = self.fix_date(
                obj['fecha_presentacion'],
            )
            return obj
        else:
            return "already in database"

    def extract_metadata(self, obj):
        """
        Using the ``numero_proyecto`` finds out if already in database. If
        false, it will try to download the metadata for such a project and
        return it. If we already have that data in the database, will will
        return "done_already"
        :param obj: {'numero_proyecto', 'titulo', 'seguimiento_page'}
        :return: metadata for proyecto de ley, "done_already"
        """
        try:
            Proyecto.objects.get(numero_proyecto=obj['numero_proyecto'])
            return "already in database"
        except Proyecto.DoesNotExist:
            # not in database
            pass

        project_soup = self.get(obj['seguimiento_page'])

        this_metadata = dict()
        for item in project_soup.find_all("input"):
            if item['name'] == "CodIni":
                this_metadata['codigo'] = item['value']
            if item['name'] == "CodIni_web_1":
                this_metadata['numero_proyecto'] = item['value']
            if item['name'] == "fechapre":
                this_metadata['fecha_presentacion'] = item['value']
            if item['name'] == "DesPropo":
                this_metadata['proponente'] = item['value']
            if item['name'] == "DesGrupParla":
                this_metadata['grupo_parlamentario'] = item['value']
            if item['name'] == "SumIni":
                this_metadata['titulo'] = item['value']
            if item['name'] == "NomCongre":
                this_metadata['congresistas'] = self.parse_names(item['value'])
            if item['name'] == "CodIniSecu":
                this_metadata['iniciativas_agrupadas'] = item['value']
            if item['name'] == "NumLey":
                this_metadata['numero_de_ley'] = item['value']
            if item['name'] == "TitLey":
                this_metadata['titulo_de_ley'] = item['value']
            if item['name'] == "NombreDeLaComision":
                this_metadata['nombre_comision'] = item['value']

        exp = 'http://www2.congreso.gob.pe/sicr/tradocestproc' \
              '/Expvirt_2011.nsf/visbusqptramdoc/'
        expediente = "%s%s%s" % (exp,
                                 this_metadata['codigo'],
                                 '?opendocument',
                                 )
        this_metadata['expediente'] = expediente
        this_metadata['pdf_url'] = self.extract_pdf_url(
            expediente,
            this_metadata['codigo'],
        )
        this_metadata['seguimiento_page'] = obj['seguimiento_page']
        return this_metadata

    def save_project(self, obj):
        print("Saving project")

