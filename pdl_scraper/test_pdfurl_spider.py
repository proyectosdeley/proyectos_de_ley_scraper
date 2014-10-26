import os
import unittest

from scrapy.http import TextResponse, Request

from pdl_scraper.spiders.pdfurl_spider import PdfUrlSpider


class TestPdfUrlSpider(unittest.TestCase):

    def setUp(self):
        self.spider = PdfUrlSpider()

    def test_find_pdfurl(self):
        codigos = (
            '00001',
            '03847',
            '00864',
            '00963',
            '01367',
            '00052',
            '00253',
            '00313',
            '00666',
        )
        expected = (
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/e8ad7d6747e75b8e052578df005a92ab/$FILE/00001.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/4465dd7d442d1a6d05257d65007d0796/$FILE/PL03847021014.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/e58512d0bfb9118d052579bb0054c0e2/$FILE/PL00864080312.-.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/72dfe9f6ee7af28a052579d000043256/$FILE/PL00963280312....pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/0/8e0331a84969f79305257a4b007a7b2b/$FILE/01367300712.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/d18f1338ca3a643b052578f1007a96ba/$FILE/00052PL1882011.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/db59e670c91ac96b05257913006ebf4b/$FILE/PL00253220911---.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/ad4b72e8abf4e2f20525792100085776/$FILE/PL00313051011,.pdf',
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/be68adfea28d33bd05257976004f91d3/$FILE/PL0066629122011-..pdf',
        )
        for i in range(len(codigos)):
            codigo = codigos[i]
            filename = codigo + '.html'
            response = fake_response_from_file(filename)
            result = self.spider.find_pdfurl(codigo, response)
            self.assertEqual(expected[i], result)


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
        file_path = os.path.join(responses_dir, 'test_spiders_data', filename)
    else:
        file_path = filename

    file_content = open(file_path, 'r').read()

    response = TextResponse(url=url, request=request, body=file_content)
    response._encoding = 'latin-1'
    return response
