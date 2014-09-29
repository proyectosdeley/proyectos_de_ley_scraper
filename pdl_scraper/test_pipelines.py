#!-*- encoding: utf-8 -*-
import datetime
import unittest

from pdl_scraper.pipelines import PdlScraperPipeline
from pdl_scraper.spiders.proyecto_spider import ProyectoSpider


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = PdlScraperPipeline()
        self.item = dict(fecha_presentacion= u'10/10/2013',
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

    def test_process_item(self):
        result_item = self.pipeline.process_item(self.item, ProyectoSpider)
        self.assertEqual(result_item['fecha_presentacion'],
                         datetime.date(2013, 10, 10))
        self.assertEqual(result_item['congresistas'][0:33], u'Espinoza Cruz, '
                                                      u'Marisol; Abugattás')
        self.assertEqual(result_item['seguimientos'][0],
                         (datetime.date(2014, 8, 28), u'Decretado a... Economía'))

    def test_save_item(self):
        self.pipeline.save_item(self.item)