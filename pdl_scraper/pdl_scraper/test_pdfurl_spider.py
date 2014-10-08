import os
import unittest

from scrapy.http import TextResponse, Request

from pdl_pdfurl.spiders.pdfurl_spider import PdfUrlSpider


class TestPdfUrlSpider(unittest.TestCase):

    def setUp(self):
        self.spider = PdfUrlSpider()

    def test_find_pdfurl(self):
        codigo = '00001'
        filename = codigo + '.html'
        response = fake_response_from_file(filename)
        result = self.spider.find_pdfurl(codigo, response)
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc' \
                   '/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/e8ad7d6747e75b8e052578df005a92ab/$FILE/00001.pdf'
        self.assertEqual(expected, result)

        codigo = '03847'
        filename = codigo + '.html'
        response = fake_response_from_file(filename)
        result = self.spider.find_pdfurl(codigo, response)
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/4465dd7d442d1a6d05257d65007d0796/$FILE/PL03847021014.pdf'
        self.assertEqual(expected, result)


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
        file_path = os.path.join(responses_dir, 'test_data', filename)
    else:
        file_path = filename

    file_content = open(file_path, 'r').read()

    response = TextResponse(url=url, request=request, body=file_content)
    response._encoding = 'latin-1'
    return response
