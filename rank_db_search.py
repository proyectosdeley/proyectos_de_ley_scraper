# -*- coding: utf-8 -*-
import datetime
import difflib
import re

import dataset

db = dataset.connect("postgresql://postgres:mysqlboriska@localhost:5432/pdl")

items = [
    {
        'fecha_publicacion': '26/06/2014',
        'texto': 'Asistencia y votación - Primera votación',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument',
        'pdf_link': 'http://some_pdf_link.pdf1',
    },
    {
        'fecha_publicacion': '26/06/2014',
        'texto': 'Asistencia y votación - Segunda votación',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument',
        'pdf_link': 'http://some_pdf_link.pdf2',
    },
    {
        'fecha_publicacion': '27/06/2014',
        'texto': 'Some other event',
        'expediente_url': 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument',
        'pdf_link': 'http://some_pdf_link.pdf3',
    },
]


def get_fechas(items):
    """
    :param items:
    :return: List of fechas in all our items.
    """
    fechas = []
    append = fechas.append
    for item in items:
        if item['fecha_publicacion'] not in fechas:
            append(item['fecha_publicacion'])

    return fechas


def update_insert_by_fecha(fecha, items):
    items_to_process = []
    append = items_to_process.append
    for item in items:
        if item['fecha_publicacion'] == fecha:
            append(item)


def update_insert_items(items):
    """
    If there are not items in our database for these dates, insert, else
    replace.

    :param items:
    :return:
    """
    fechas = get_fechas(items)

    for fecha in fechas:
        update_insert_by_fecha(fecha, items)
    """
    table = db['pdl_proyecto']
    res = table.find_one(expediente=expediente_url)
    if res is not None:
        # Need to replace to 1ra and 2da
        print(texto)
        pattern = re.compile("PRIMERA", re.I)
        texto = pattern.sub("1ra", texto)

        pattern = re.compile("SEGUNDA", re.I)
        texto = pattern.sub("2da", texto).decode("utf-8")

        fecha_obj = datetime.datetime.strptime(fecha_publicacion, '%d/%m/%Y')
        fecha_iso = datetime.datetime.strftime(fecha_obj, '%Y-%m-%d')
        proyecto_id = res['id']
        # Query events in seguimientos with our date and proyecto_id
        res_events = db.query("select * from pdl_seguimientos where proyecto_id=%s and "
                              "fecha='%s'"
                              % (str(proyecto_id), fecha_iso))
        ratio = 0
        best_match = {}
        for i in res_events:
            s = difflib.SequenceMatcher(lambda x: x == " ", texto, i['evento'])
            if s.real_quick_ratio() > ratio:
                ratio = s.real_quick_ratio()
                best_match = i
        print(best_match)
        print(ratio)
    """


update_insert_items(items)
