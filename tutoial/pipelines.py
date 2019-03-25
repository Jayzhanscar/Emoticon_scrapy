# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class TextPipeline(object):
    """
    数据存储之前对数据进行处理或者修改相应的格式
    """
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['title']:
            if len(item['title']) > self.limit:
                item['title'] = item['title'][0: self.limit].rstrip() + '...'

            return item
        else:
            return DropItem('Missing Text')
    
    def open_spider(self, spider):
        """
        在spider打开之前被调用
        :param spider:
        :return:
        """
        pass
    
    def close_spider(self, spider):
        """
        在spider关闭之前被调用
        :param spider:
        :return:
        """
        pass


class MongoPipeline(object):
    """ mongo连接 """
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    """ mysql连接 """
    
    def __init__(self, host, port, data_name, user, password):
        self.host = host
        self.port = port
        self.data_name = data_name
        self.user = user
        self.password = password
        self.db = None
        self.cursor = None
        self.client = None
        self.tables = ''
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('POST'),
            data_name=crawler.settings.get('DATA_NAME'),
            user=crawler.settings.get('USER'),
            password=crawler.settings.get('PASSWORD'),
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.data_name,
                                  charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join['%s'] * len(data)
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
    
    def close_spider(self, spider):
        self.client.close()


class ImagePipeline(ImagesPipeline):
    """ 继承Scrapy imagePipeline 类 """
    # TODO 未完成下载
    
    def file_path(self, request, response=None, info=None):
        url = request.url
        print('this is url', url)
        file_name = url.split('/')[-1]
        
        return file_name
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('image download failed')

        item['image_paths'] = image_paths
        return item
    
    def get_media_requests(self, item, info):
        
        yield Request(item['path'])

