# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PdlScraperItem(Item):
    # define the fields for your item here like:
    codigo = Field()
    numero_proyecto = Field()
    short_url = Field()
    congresistas = Field()
    fecha_presentacion = Field()
    titulo = Field()
    expediente = Field()
    seguimiento_page = Field()
    proponente = Field()
    grupo_parlamentario = Field()
    iniciativas_agrupadas = Field()
    nombre_comision = Field()
    titulo_de_ley = Field()
    numero_de_ley = Field()
    time_created = Field()


class SeguimientosItem(Item):
    codigo = Field()
    seguimientos = Field()


class IniciativaItem(Item):
    codigo = Field()
    iniciativas_agrupadas = Field()


class PdlPdfUrlItem(Item):
    # define the fields for your item here like:
    pdf_url = Field()
    codigo = Field()