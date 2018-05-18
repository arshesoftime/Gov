# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MDPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'chongqing':
            self.db['chongqing'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        elif spider.name == 'sh':
            self.db['shanghai'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        elif spider.name == 'zj':
            self.db['zhejiang'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        elif spider.name == 'hlj':
            self.db['heilongjiang'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        elif spider.name == 'bj':
            self.db['beijing'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        elif spider.name == 'hn':
            self.db['hunan'].update({'detail_url': item['detail_url']}, {'$set': item}, True)
        return item
