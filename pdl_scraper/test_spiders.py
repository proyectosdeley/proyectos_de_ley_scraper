#!-*- encoding: utf-8 -*-
import os
import unittest

from scrapy.http import TextResponse, Request

from pdl_scraper.spiders.proyecto_spider import ProyectoSpider


class TestProyectoSpider(unittest.TestCase):
    def setUp(self):
        self.spider = ProyectoSpider()

    def test_parse_pdfurl(self):
        filename = os.path.join('test_spiders_data', '02764.html')
        results = self.spider.parse_item(fake_response_from_file(filename))
        print(results.meta['item'])
        item = results.meta['item']
        self.assertEqual(item['numero_proyecto'], u'02764/2013-CR')
        self.assertEqual(item['codigo'], u'02764')
        self.assertEqual(item['congresistas'][0:10], u'Elias Aval')
        self.assertEqual(item['short_url'], u'4zhube')
        self.assertEqual(item['fecha_presentacion'], u'10/10/2013')
        self.assertEqual(item['titulo'], u'Propone Ley Universitaria')
        self.assertEqual(item['expediente'], u'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument')
        self.assertEqual(item['seguimiento_page'],
                         u'http://www.example.com')
        self.assertEqual(item['proponente'], u'Congreso')
        self.assertEqual(item['grupo_parlamentario'],
                         u'Grupo Parlamentario Fuerza Popular')
        self.assertEqual(item['iniciativas_agrupadas'][0:5], u'00154')
        self.assertEqual(item['nombre_comision'],
                        u'Comisión de Educación  Juventud y Deporte')
        self.assertEqual(item['titulo_de_ley'], u'LEY UNIVERSITARIA')
        self.assertEqual(item['numero_de_ley'], u'Ley Nº: 30220')


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
