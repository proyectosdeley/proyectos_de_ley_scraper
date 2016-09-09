# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import pytz
import re
import six
import unicodedata

from scrapy import log

from models import db_connect


def convert_to_ascii(my_string):
    return unicodedata.normalize(
        'NFKD',
        my_string,
    ).encode('ascii', 'ignore').decode('utf-8')


class PdlScraperPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'proyecto':
            item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
            item['congresistas'] = self.parse_names(item['congresistas'])
            item['congresistas_ascii'] = convert_to_ascii(item['congresistas'])
            item['iniciativas_agrupadas'] = self.parse_iniciativas(item['iniciativas_agrupadas'])
            item['time_created'] = datetime.utcnow().replace(tzinfo=pytz.utc)
            item['time_edited'] = datetime.utcnow().replace(tzinfo=pytz.utc)
            self.save_item(item)
            return item
        return item

    def save_item(self, item):
        db = db_connect()
        table = db['pdl_proyecto']

        db.query("SELECT setval('pdl_proyecto_id_seq', (SELECT MAX(id) FROM pdl_proyecto)+1)")
        is_in_db = table.find_one(
            codigo=item['codigo'],
            legislatura=item['legislatura'],
        )
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
            mydate = datetime.date(datetime.strptime(string, '%d/%m/%Y'))
        except ValueError:
            # mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
            log.msg("fecha_presentacion was not in the right format.")
            string = "1970-01-01"
            mydate = datetime.date(datetime.strptime(string, '%Y-%m-%d'))
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

class SeguimientosPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'seguimientos':
            item['seguimientos'] = self.fix_seguimientos_list(item['seguimientos'])
            log.msg(item['codigo'])
            log.msg(item['seguimientos'])
            self.save_seguimientos(item)
            return item
        return item

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

    def save_seguimientos(self, item):
        """
        Try to save a list of tuples to Seguimientos model if they don't
        exist already.
        """
        log.msg("Try to save seguimientos.")
        db = db_connect()

        # get proyect id for these seguimientos
        table = db['pdl_proyecto']
        res = table.find_one(codigo=item['codigo'])
        if res is None:
            log.msg("There is no project with that code: %s" % item['codigo'])
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
                log.msg("Trying to save evento %s, proyecto_id %s fecha %s" %
                        (
                         new_i['evento'],
                         new_i['proyecto_id'],
                         datetime.strftime(new_i['fecha'], '%Y-%m-%d'),
                         )
                )

                res2 = table.find_one(
                    fecha=datetime.strftime(new_i['fecha'], '%Y-%m-%d'),
                    evento=new_i['evento'],
                    proyecto_id=new_i['proyecto_id']
                )
                if res2 is None:
                    # not in database
                    log.msg("This event is not in the database.")
                    append(new_i)
                else:
                    log.msg("This event is already in the database.")
            table.insert_many(seguimientos_to_save)


class IniciativasPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'iniciativa':
            item['iniciativas_agrupadas'] = self.parse_iniciativas(item['iniciativas_agrupadas'])
            item['time_edited'] = datetime.utcnow().replace(tzinfo=pytz.utc)
            log.msg(item['codigo'])
            self.save_iniciativas(item)
            return item
        return item

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

    def save_iniciativas(self, item):
        """
        Try to save a list of tuples to Seguimientos model if they don't
        exist already.
        """
        log.msg("Try to save iniciativas.")
        db = db_connect()

        # get proyect id for these seguimientos
        table = db['pdl_proyecto']
        table.update(item, ['codigo'])


class PdlPdfurlPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'pdfurl':
            # save pdfurl
            log.msg("Try saving pdf_url to database: %s." % item['codigo'])
            db = db_connect()
            table = db['pdl_proyecto']
            table.update(item, ['codigo'])
            return item
        return item


class UpdaterPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'updater':
            log.msg("Try saving item to database: %s." % item['codigo'])
            db = db_connect()
            table = db['pdl_proyecto']
            table.update(item, ['codigo'])
            return item
        return item


class UpdateFechaPresentacionPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'fecha_presentacion':
            item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
            self.save_item(item)
            return item
        return item

    def save_item(self, item):
        db = db_connect()
        table = db['pdl_proyecto']
        table.update(item, ['codigo'])
        log.msg("Saving project: %s" % item['codigo'])

    def fix_date(self, string):
        """
        Takes an string date from Proyecto and converts it to Date object.
        :param string: "08/28/2014"
        :return: date(2014, 08, 28)
        """
        try:
            mydate = datetime.date(datetime.strptime(string, '%d/%m/%Y'))
        except ValueError:
            # mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
            log.msg("fecha_presentacion was not in the right format.")
            string = "1970-01-01"
            mydate = datetime.date(datetime.strptime(string, '%Y-%m-%d'))
        return mydate


class ExpedientePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'expediente':
            item['proyecto_id'] = self.get_proyecto_id(item)
            item['fecha'] = self.fix_date(item['fecha'])
            del item['expediente_url']
            self.save_expediente_items(item)
            return item
        return item

    def get_proyecto_id(self, item):
        """
        :param item: seguimientos
        :return: proyecto_id from pdl_seguimientos table
        """
        db = db_connect()
        table = db['pdl_proyecto']
        res = table.find_one(expediente=item['expediente_url'])
        if res is None:
            log.msg("There is no project with that expediente_url: %s" % item['expediente_url'])
        else:
            return res.get('id')

    def save_expediente_items(self, item):
        """
        Try to save if they don't exist already.
        """
        log.msg("Try to save events in expedientes.")
        db = db_connect()
        table = db['pdl_expedientes']

        if item['fecha'] != '':
            # Sometimes we scrap title when there are no events. The fecha will
            # be empty, so continue and ignore this item.
            res = table.find_one(
                fecha=item['fecha'],
                evento=item['evento'],
                proyecto_id=item['proyecto_id'],
                pdf_url=item['pdf_url'],
            )
            if res is None:
                # not in database
                log.msg("This event is not in the database.")
                table.insert(item)
            else:
                log.msg("This event '%s' is already in the database." % item['evento'])

    def fix_date(self, string):
        """
        Takes an string date from Proyecto and converts it to Date object.
        :param string: "08/28/14"
        :return: 2014-08-28
        """
        try:
            mydate = datetime.strptime(string, '%d/%m/%y')
        except ValueError:
            mydate = ''

        if mydate != '':
            mydate = datetime.strftime(mydate, '%Y-%m-%d')
        return mydate
