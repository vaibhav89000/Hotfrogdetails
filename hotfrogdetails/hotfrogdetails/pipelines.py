# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class HotfrogdetailsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("hotfrogdetails.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS detail""")
        self.curr.execute("""create table detail(
        website_name text,
        website_link text,
        phone text,
        business_info text,
        find text,
        near text,
        email text,
        website text
        )""")
        # pass

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into detail values (?,?,?,?,?,?,?,?)""",(
            item['website_name'],
            item['website_link'],
            item['phone'],
            item['business_info'],
            item['find'],
            item['near'],
            item['email'],
            item['website']
        ))
        self.conn.commit()
