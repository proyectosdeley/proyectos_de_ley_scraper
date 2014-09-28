#!-*- encoding: utf-8 -*-
import os
import unittest

from scrapy.http import TextResponse, Request

from pdl_scraper.spiders.proyecto_spider import ProyectoSpider


class TestProyectoSpider(unittest.TestCase):
    def setUp(self):
        self.spider = ProyectoSpider()

    def test_parse(self):
        filename = os.path.join('test_spiders_data', '02764.html')
        results = self.spider.parse_item(fake_response_from_file(filename))
        for item in results:
            self.assertEqual(u'02764/2013-CR', item['numero_proyecto'])
            self.assertEqual(u'02764', item['codigo'])
            self.assertEqual(u'Elias Aval', item['congresistas'][0:10])
            self.assertEqual(u'', item['short_url'])
            self.assertEqual(u'10/10/2013', item['fecha_presentacion'])
            self.assertEqual(u'Propone Ley Universitaria', item['titulo'])
            self.assertEqual(u'', item['expediente'])
            self.assertEqual(u'', item['pdf_url'])
            self.assertEqual(u'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2011.nsf/Sicr/TraDocEstProc/CLProLey2011.nsf/PAporNumeroInverso/A4604A57E03E482405257C01000B1980?opendocument',
                             item['seguimiento_page'])
            self.assertEqual(u'Congreso', item['proponente'])
            self.assertEqual(u'Grupo Parlamentario Fuerza Popular',
                             item['grupo_parlamentario'])
            self.assertEqual(u'00154', item['iniciativas_agrupadas'][0:5])
            self.assertEqual(u'Comisión de Educación  Juventud y Deporte',
                             item['nombre_comision'])
            self.assertEqual(u'LEY UNIVERSITARIA', item['titulo_de_ley'])
            self.assertEqual(u'Ley Nº: 30220', item['numero_de_ley'])

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

    response = TextResponse(url=url,
        request=request,
        body=file_content)
    response._encoding = 'latin-1'
    return response