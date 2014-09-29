# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import logging
import re

from models import db_connect


class PdlScraperPipeline(object):
    def process_item(self, item, spider):
        item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
        item['congresistas'] = self.parse_names(item['congresistas'])
        item['seguimientos'] = self.fix_seguimientos_list(item['seguimientos'])
        self.save_item(item)
        return item

    def save_item(self, item):
        db = db_connect()
        table = db['pdl_proyecto']

        db.query("SELECT setval('pdl_proyecto_id_seq', (SELECT MAX(id) FROM pdl_proyecto)+1)")
        is_in_db = table.find_one(codigo=item['codigo'])
        if is_in_db is None:
            logging.debug(">> %s is not in db" % item['codigo'])
            # get last used id in our database
            table.insert(item)
            logging.debug("Saving project: %s" % item['codigo'])
        else:
            logging.debug("%s is found in db" % item['codigo'])
            logging.debug("not saving")

    def save_seguimientos(self, item):
        """
        Try to save a list of tuples to Seguimientos model if they don't
        exist already.
        """
        db = db_connect()

        # get proyect id for these seguimientos
        table = db['pdl_proyecto']
        res = table.find_one(codigo=item['codigo'])
        if res is None:
            logging.critical("There is no project with that code: %s" % item['codigo'])
        else:
            # save
            table = db['pdl_seguimientos']
            proyecto_id = res.get('id')
            seguimientos_to_save = []
            append = seguimientos_to_save.append
            for i in item['seguimientos']:
                new_i = {'fecha': i[0],
                         'evento': i[1],
                         'proyecto_id': proyecto_id,
                }
                logging.debug(new_i)

                res = table.find_one(fecha=datetime.strftime(new_i['fecha'],
                                                             '%Y-%m%-d'),
                                     evento=new_i['evento'],
                                     proyecto_id=new_i['proyecto_id'])
                if res is None:
                    # not in database
                    append(new_i)
            table.insert_many(seguimientos_to_save)

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