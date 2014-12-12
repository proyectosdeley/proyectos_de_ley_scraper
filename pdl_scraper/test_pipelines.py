#!-*- encoding: utf-8 -*-
import datetime
import unittest

from pdl_scraper.pipelines import PdlScraperPipeline
from pdl_scraper.pipelines import ExpedientePipeline
from pdl_scraper.pipelines import SeguimientosPipeline
from pdl_scraper.pipelines import IniciativasPipeline
from pdl_scraper.spiders.proyecto_spider import ProyectoSpider
from pdl_scraper.spiders.seguimientos_spider import SeguimientoSpider
from pdl_scraper.spiders.iniciativas_spider import IniciativaSpider
from pdl_scraper.models import db_connect


ITEM = dict(fecha_presentacion=datetime.date(2013, 10, 10),
            codigo=u'011',
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
            )


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
                         time_created='',
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

    def test_parse_iniciativas(self):
        iniciativas_agrupadas = u'00154, 00353, 00368, 00484, 00486'
        result = self.pipeline.parse_iniciativas(iniciativas_agrupadas)
        expected = [
            u'00154',
            u'00353',
            u'00368',
            u'00484',
            u'00486',
        ]
        self.assertEqual(expected, result)

        iniciativas_agrupadas = u''
        result = self.pipeline.parse_iniciativas(iniciativas_agrupadas)
        expected = ''
        self.assertEqual(expected, result)

        iniciativas_agrupadas = []
        result = self.pipeline.parse_iniciativas(iniciativas_agrupadas)
        expected = ''
        self.assertEqual(expected, result)

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

        time_created = result_item['time_created']
        self.assertEqual(time_created.date(),
                         datetime.date.today())
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

    def test_convert_accented_name_to_slug(self):
        name = "Yóní Páchécó Soy"
        expected = "yoni_pacheco_soy/"
        result = self.pipeline.convert_name_to_slug(name)
        self.assertEqual(expected, result)

    def test_fix_date(self):
        string = '13/10/2012'
        expected = datetime.date(2012, 10, 13)
        result = self.pipeline.fix_date(string)
        self.assertEqual(expected, result)

    def test_fix_date_exception(self):
        string = '13/13/2012'
        expected = datetime.date(1970, 1, 1)
        result = self.pipeline.fix_date(string)
        self.assertEqual(expected, result)


class TestSeguimientosPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = SeguimientosPipeline()

    def test_fix_seguiminetos_list(self):
        events = ['13/10/2012 Evento1', '14/11/2013 Evento2']
        expected = [
            (datetime.date(2012, 10, 13), 'Evento1'),
            (datetime.date(2013, 11, 14), 'Evento2'),
        ]
        result = self.pipeline.fix_seguimientos_list(events)
        self.assertEqual(expected, result)

    def test_save_seguimientos(self):
        db = db_connect()
        table = db['pdl_proyecto']
        table.insert(ITEM)
        ITEM['seguimientos'] = [
            (datetime.date(2012, 10, 13), 'Evento1'),
            (datetime.date(2013, 11, 14), 'Evento2'),
        ]
        db.query("delete from pdl_seguimientos where 1=1")
        self.pipeline.save_seguimientos(ITEM)

        res = db.query("select * from pdl_seguimientos")
        result = []
        for i in res:
            result.append(i)
        expected = 2
        self.assertEqual(expected, len(result))

    def test_process_item(self):
        ITEM['seguimientos'] = ['13/10/2012 Evento1', '14/11/2013 Evento2']
        expected = [
            (datetime.date(2012, 10, 13), 'Evento1'),
            (datetime.date(2013, 11, 14), 'Evento2'),
        ]
        result = self.pipeline.process_item(ITEM, SeguimientoSpider)
        self.assertEqual(expected, result['seguimientos'])


class TestIniciativasPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = IniciativasPipeline()
        self.db = db_connect()

    def test_process_item(self):
        item = {
            'iniciativas_agrupadas': '02134, 02324',
            'codigo': '02764',
        }
        result = self.pipeline.process_item(item, IniciativaSpider)
        expected = ['02134', '02324']
        self.assertEqual(expected, result['iniciativas_agrupadas'])

    def test_process_item_return(self):
        item = {
            'iniciativas_agrupadas': '02134, 02324',
            'codigo': '02764',
            }
        result = self.pipeline.process_item(item, SeguimientoSpider)
        expected = '02134, 02324'
        self.assertEqual(expected, result['iniciativas_agrupadas'])

    def test_parse_iniciativas(self):
        string = '02134,03421'
        expected = ['02134', '03421']
        result = self.pipeline.parse_iniciativas(string)
        self.assertEqual(expected, result)

    def test_parse_iniciativas_list(self):
        string = ['02130']
        result = self.pipeline.parse_iniciativas(string)
        expected = ''
        self.assertEqual(expected, result)

    def test_parse_iniciativas_empty(self):
        string = ' '
        expected = ''
        result = self.pipeline.parse_iniciativas(string)
        self.assertEqual(expected, result)

    def test_save_iniciativas(self):
        item = {
            'codigo': '02734',
            'iniciativas_agrupadas': ['02134', '03421'],
        }
        table = self.db['pdl_proyecto']
        self.pipeline.save_iniciativas(item)
        res = table.find_one(codigo='02734')
        self.assertEqual('{02134,03421}', res['iniciativas_agrupadas'])


class TestExpedientePipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = ExpedientePipeline()
        self.db = db_connect()

    def test_expediente_items(self):
        item = {
            'evento': 'Ley modificatoria de la Ley 27314, Ley General',
	        'fecha': '',
            'pdf_url': u'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/94b5fe12ac4be3b705257c9c0008daad/$FILE/PL03279140314.pdf',
	        'proyecto_id': 3280,
        }
        self.pipeline.save_expediente_items(item)
        table = self.db['pdl_expediente']
        result = table.find_one(proyecto_id=3280)
        expected = None
        self.assertEqual(expected, result)

    def test_fix_date(self):
        string = "13/04/14"
        result = self.pipeline.fix_date(string)
        expected = "2014-04-13"
        self.assertEqual(expected, result)

    def test_fix_date_return_empty(self):
        string = "04/13/14"
        result = self.pipeline.fix_date(string)
        expected = ""
        self.assertEqual(expected, result)
