# This connects and inserts the data into MongoDB


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import hashlib

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
        item_id = self.compute_id(item)
        
        # If a duplicate gets found, raise an error
        if self.db[self.COLLECTION_NAME].find_one({"_id":item_id}):
            raise DropItem(f"Duplicate found: {item}")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
        return item

    def compute_id(self, item):
        url = item["url"] # get the url

        # returns the hashvalues of the url
        # url gets encoded to bytes and then sha256() produces a fixed 64-character hex string no matter how long input is 
        # after we get hexstring, the .hexdigest() turns it into readable hex string instead of raw bytes
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

# class BooksPipeline:
#     def process_item(self, item, spider):
#         return item
