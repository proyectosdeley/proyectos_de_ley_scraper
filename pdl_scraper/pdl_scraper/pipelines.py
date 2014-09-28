# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import re
from models import db_connect
from scrapy.exceptions import DropItem

class PdlScraperPipeline(object):
    def process_item(self, item, spider):
        item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
        item['congresistas'] = self.parse_names(item['congresistas'])
        item['seguimientos'] = self.fix_seguimientos_list(item['seguimientos'])
        return item

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

    def fix_seguimientos_list(self, events):
        """
        :param events: seguimientos
        :return: a tuple (date object, event string)
        """
        new_events = []
        append = new_events.append
        for i in events:
            i_strip = i.strip()
            if i_strip != '':
                res = re.search('^([0-9]{2}/[0-9]{2}/[0-9]{4})\s+(.+)', i_strip)
                if res:
                    d = datetime.strptime(res.groups()[0], '%d/%m/%Y')
                    event = re.sub('\s+', ' ', res.groups()[1])
                    append((datetime.date(d), event))
        return new_events