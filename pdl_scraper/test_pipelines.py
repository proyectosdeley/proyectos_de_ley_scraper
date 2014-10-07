#!-*- encoding: utf-8 -*-
import datetime
import unittest

from pdl_scraper.pipelines import PdlScraperPipeline
from pdl_scraper.spiders.proyecto_spider import ProyectoSpider
from pdl_scraper.models import db_connect


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = PdlScraperPipeline()
        self.item = dict(fecha_presentacion=u'10/10/2013',
                         codigo=u'11111111111',
                         numero_proyecto=u'11111111111/2014-CR',
                         short_url=u'',
                         titulo='',
                         expediente='',
                         pdf_url='',
                         time_created=datetime.date.today(),
                         time_edited=datetime.date.today(),
                         seguimiento_page='',
                         grupo_parlamentario='',
                         iniciativas_agrupadas=u'00154, 00353, 00368, 00484, 00486',
                         nombre_comision='',
                         numero_de_ley='',
                         titulo_de_ley='',
                         proponente='',
                         congresistas=u'Espinoza Cruz  Marisol,Abugattás '
                                      u'Majluf  Daniel Fernando,Acha Roma'
                                      u'ni  Walter,Apaza Condori  Emiliano,'
                                      u'Nayap Kinin  Eduardo,Reynaga'
                                      u'Soto  Jhon Arquimides,Valencia '
                                      u'Quiroz  Jaime Ruben',
                         seguimientos=[
                             '',
                             u'28/08/2014 Decretado a... Economía',
                             u' ',
                         ]
        )
        self.db = db_connect()

    def test_process_item(self):
        result_item = self.pipeline.process_item(self.item, ProyectoSpider)
        self.assertEqual(result_item['iniciativas_agrupadas'], [
            u'00154',
            u'00353',
            u'00368',
            u'00484',
            u'00486',
        ])
        self.assertEqual(result_item['fecha_presentacion'],
                         datetime.date(2013, 10, 10))
        self.assertEqual(result_item['congresistas'][0:33], u'Espinoza Cruz, '
                                                      u'Marisol; Abugattás')

    def test_save_item(self):
        # database should have it
        db = db_connect()
        table = db['pdl_proyecto']
        self.assertIsNotNone(table.find_one(codigo=self.item['codigo']))

        self.pipeline.save_item(self.item)

        # delete item
        table.delete(codigo=self.item['codigo'])

    def test_save_slug(self):
        db = db_connect()
        table = db['pdl_slug']
        fixed_item = self.pipeline.process_item(self.item, ProyectoSpider)
        fixed_item['congresistas'] = u'Pacheco Soy, Yóní'
        self.pipeline.save_slug(fixed_item)

        res = table.find_one(slug='pacheco_soy_yoni/')
        self.assertEqual(res['nombre'], u'Pacheco Soy, Yóní')

        res = self.pipeline.save_slug(fixed_item)
        self.assertEqual(res, 'slug already in database')

        table.delete(slug='pacheco_soy_yoni/')
