#!-*- encoding: utf-8 -*-
import datetime
import unittest

from pdl_scraper.pipelines import PdlScraperPipeline
from pdl_scraper.spiders.proyecto_spider import ProyectoSpider


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = PdlScraperPipeline()
        self.item = dict(fecha_presentacion= u'10/10/2013')

    def test_process_item(self):
        result_item = self.pipeline.process_item(self.item, ProyectoSpider)
        self.assertEqual(result_item['fecha_presentacion'],
                         datetime.date(2013, 10, 10))
