# -*- coding: utf-8 -*-
import datetime
import difflib
import re

import dataset

db = dataset.connect("postgresql://postgres:mysqlboriska@localhost:5432/pdl")

items = [
    {
        'fecha': '25/06/2012',
        'evento': '2Asistencia y votación - Primera votación',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/01180?opendocument',
        'pdf_url': 'http://some_pdf_link.pdf1',
    },
    {
        'fecha': '25/06/2012',
        'evento': '2Asistencia y votación - Segunda votación',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/01180?opendocument',
        'pdf_url': 'http://some_pdf_link.pdf2',
    },
    {
        'fecha': '27/06/2014',
        'evento': '1Some other event',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/01180?opendocument',
        'pdf_url': 'http://some_pdf_link.pdf3',
    },
]


def delete_from_db_if_match(item, proyecto_id):
    """
    If found in database delete. We can replace it soon afterwards.
    :param item:
    :param proyecto_id:
    :return:
    """
    table = db['pdl_seguimientos']
    table.delete(proyecto_id=proyecto_id, fecha=item['fecha'])


def get_proyecto_id_from_expediente_url(item):
    table = db['pdl_proyecto']
    res = table.find_one(expediente=item['expediente_url'])
    if res is not None:
        return res['id']
    else:
        return None


def update_insert_items(items):
    """
    If there are not items in our database for these dates, insert, else
    replace.

    :param items:
    :return:
    """

    for item in items:
        tmp_fecha = datetime.datetime.strptime(item['fecha'], '%d/%m/%Y')
        item['fecha'] = datetime.datetime.strftime(tmp_fecha, '%Y-%m-%d')
        proyecto_id = get_proyecto_id_from_expediente_url(item)
        item['proyecto_id'] = proyecto_id
        delete_from_db_if_match(item, proyecto_id)

    for item in items:
        table = db['pdl_seguimientos']
        del item['expediente_url']
        table.insert(item)
        print item


update_insert_items(items)
