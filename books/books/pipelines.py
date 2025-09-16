# This connects and inserts the data into MongoDB


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class MongoPipeline:
    # define the name of collection(s)
    COLLECTION_NAME = "books"

    # initalizes the pipeline with MongoDB URI and db name
    # able to access info since its getting fetched from Crawler using the .from_crawler() class method
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # allows all core scrapy components, such as settings 
    # below you are able to get the MongoDB settings from settings.py through crawler
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )
    
    # connect to the Mongo DB when spider starts
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    # close the connection when spider ends
    def close_spider(self, spider):
        self.client.close()
    
    # insert each scraped item into the MongoDB collection
    # core functionality of a pipeline
    def process_item(self, item, spider):
        self.db[self.COLLECTION_NAME].insert_one(item).asdict()
        return item


class BooksPipeline:
    def process_item(self, item, spider):
        return item
