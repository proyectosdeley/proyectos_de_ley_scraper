# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import Proyecto, db_connect, create_proyecto_table

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class PdlScraperPipeline(object):
class ProyectoPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_proyecto_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        return item
