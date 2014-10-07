# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy import log
import re
import unicodedata

import six

from models import db_connect


class PdlScraperPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'proyecto':
            item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
            item['congresistas'] = self.parse_names(item['congresistas'])
            item['iniciativas_agrupadas'] = self.parse_iniciativas(item['iniciativas_agrupadas'])
            self.save_item(item)
            return item

    def save_item(self, item):
        db = db_connect()
        table = db['pdl_proyecto']

        db.query("SELECT setval('pdl_proyecto_id_seq', (SELECT MAX(id) FROM pdl_proyecto)+1)")
        is_in_db = table.find_one(codigo=item['codigo'])
        if is_in_db is None:
            log.msg(">> %s is not in db" % item['codigo'])
            # get last used id in our database
            table.insert(item)
            log.msg("Saving project: %s" % item['codigo'])
        else:
            log.msg("%s is found in db" % item['codigo'])
            log.msg("not saving")

    def fix_date(self, string):
        """
        Takes an string date from Proyecto and converts it to Date object.
        :param string: "08/28/2014"
        :return: date(2014, 08, 28)
        """
        try:
            mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
        except ValueError:
            mydate = datetime.date(datetime.strptime(string, '%d/%m/%Y'))
        return mydate

    def parse_names(self, string):
        """
        :param string: Person names separated by commas.
        :return: String of person names separated by colons and family names
                 separated from given names by commas.
        """
        names = ""
        for i in string.split(","):
            i = re.sub("\s{2}", ", ", i)
            names += i + "; "
        names = re.sub(";\s$", "", names)
        return names

    def parse_iniciativas(self, string):
        """
        :param string:
        :return: list of iniciativas
        """
        if type(string) == list:
            return ''

        if string.strip() == '':
            return ''

        iniciativas = string.split(",")
        iniciativas_stripped = [i.strip() for i in iniciativas]
        return iniciativas_stripped

    def save_slug(self, obj):
        db = db_connect()
        table = db['pdl_slug']
        db.query("SELECT setval('pdl_slug_id_seq', (SELECT MAX(id) FROM pdl_slug)+1)")
        for congre in obj['congresistas'].split(';'):
            congre = congre.strip()
            congre_slug = dict(nombre=congre)
            if congre is not None and congre != '':
                slug = self.convert_name_to_slug(congre)
                congre_slug['slug'] = slug

                res = table.find_one(slug=congre_slug['slug'])
                if res is None:
                    # slug doesnotexist
                    table.insert(congre_slug)
                else:
                    return "slug already in database"

    def convert_name_to_slug(self, name):
        """Takes a congresista name and returns its slug."""
        name = name.strip()
        name = name.replace(",", "").lower()
        name = name.split(" ")

        if len(name) > 2:
            i = 0
            slug = ""
            while i < 3:
                slug += name[i]
                if i < 2:
                    slug += "_"
                i += 1
            try:
                slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore')
            except TypeError:
                slug = slug.decode('utf-8')
                slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore')

            if six.PY3 is True:
                slug = str(slug, encoding="utf-8")
            else:
                slug = slug.encode("utf-8")
            return slug + "/"
