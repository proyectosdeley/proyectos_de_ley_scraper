# -*- coding: utf-8 -*-
import datetime

import dataset

db = dataset.connect("postgresql://postgres:mysqlboriska@localhost:5433/pdl")

fecha_publicacion = u'26/06/2014'
texto = u'Asistencia y votación - Primera votación'
expediente_url = u'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/02764?opendocument'

def get_ranked_item(fecha_publicacion, texto, expediente_url):
    table = db['pdl_proyecto']
    res = table.find_one(expediente=expediente_url)
    if res is not None:
        fecha_obj = datetime.datetime.strptime(fecha_publicacion, '%d/%m/%Y')
        fecha_iso = datetime.datetime.strftime(fecha_obj, '%Y-%m-%d')
        proyecto_id = res['id']
        # query events in seguimientos with our date and proyecto_id
        res_events = db.query("select * from pdl_seguimientos where proyecto_id=%s and "
                              "fecha='%s'"
                              % (str(proyecto_id), fecha_iso))
        for i in res_events:
            print i



get_ranked_item(fecha_publicacion, texto, expediente_url)
