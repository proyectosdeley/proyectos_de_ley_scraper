#!-*- encoding: utf-8 -*-
import os
import unittest

from scrapy.http import TextResponse, Request

from pdl_scraper.spiders.iniciativas_spider import IniciativaSpider


class TestSpiderIniciativa(unittest.TestCase):
    def setUp(self):
        self.spider = IniciativaSpider()

    def test_get_urls(self):
        result = self.spider.get_my_urls()
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Sicr/TraDocEstProc/CLProLey2011.nsf/PAporNumeroInverso/D36F68EDA5474A7605257CAE005690F0?opendocument'
        self.assertEqual(expected, result[0])


def fake_response_from_file(filename, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.

    taken from http://stackoverflow.com/a/12741030/3605870
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    if not filename[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, filename)
    else:
        file_path = filename

    file_content = open(file_path, 'r').read()

    response = TextResponse(url=url, request=request, body=file_content)
    response._encoding = 'latin-1'
    return response
