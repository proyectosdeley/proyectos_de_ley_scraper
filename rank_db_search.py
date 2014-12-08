# -*- coding: utf-8 -*-
import datetime
import re

import dataset

db = dataset.connect("postgresql://postgres:mysqlboriska@localhost:5433/pdl")

fecha_publicacion = '26/06/2014'
texto = 'Asistencia y votación - Primera votación'
expediente_url = 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument'

def get_ranked_item(fecha_publicacion, texto, expediente_url):
    table = db['pdl_proyecto']
    res = table.find_one(expediente=expediente_url)
    if res is not None:
        # Need to replace to 1ra and 2da
        pattern = re.compile("PRIMERA", re.I)
        texto = pattern.sub("1era", texto)

        pattern = re.compile("SEGUNDA", re.I)
        texto = pattern.sub("2da", texto)

        fecha_obj = datetime.datetime.strptime(fecha_publicacion, '%d/%m/%Y')
        fecha_iso = datetime.datetime.strftime(fecha_obj, '%Y-%m-%d')
        proyecto_id = res['id']
        # Query events in seguimientos with our date and proyecto_id
        res_events = db.query("select * from pdl_seguimientos where proyecto_id=%s and "
                              "fecha='%s'"
                              % (str(proyecto_id), fecha_iso))
        for i in res_events:
            print i['evento']



get_ranked_item(fecha_publicacion, texto, expediente_url)
