#!-*- encoding: utf-8 -*-
import os
import unittest

from _test_utils import fake_response_from_file
from pdl_scraper.spiders.iniciativas_spider import IniciativaSpider


class TestSpiderIniciativa(unittest.TestCase):
    def setUp(self):
        self.spider = IniciativaSpider()

    def test_get_urls(self):
        result = self.spider.get_my_urls()
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Sicr/TraDocEstProc/CLProLey2011.nsf/PAporNumeroInverso/D36F68EDA5474A7605257CAE005690F0?opendocument'
        self.assertEqual(expected[:118], result[0][:118])

    def test_parse(self):
        codigo = '02764'
        filename = codigo + '.html'
        response = fake_response_from_file(filename)
        result = self.spider.parse(response)
        expected = u'00154'
        self.assertEqual(expected, result.next()['iniciativas_agrupadas'][0:5])


