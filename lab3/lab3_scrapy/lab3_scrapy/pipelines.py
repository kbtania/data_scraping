# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlite3 import connect
from scrapy.exceptions import DropItem

class Lab3ScrapyPipeline:
    def process_item(self, item, spider):
        return item

class DuplicateFilterPipeline:

    def __init__(self, file_name):
        self.file_name = file_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            file_name=crawler.settings.get("DB_FILE_NAME")
        )

    def open_spider(self, spider):
        self.connection = connect(self.file_name)

    def process_item(self, item, spider):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM videocard WHERE link = ?", [item["link"]])
        if cursor.fetchone()[0] > 0:
            raise DropItem(f"Duplicate {item['link']}")        
        return item

    def close_spider(self, spider):
        self.connection.close()

class SqlitePipeline:
    def __init__(self, file_name):
        self.file_name = file_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            file_name=crawler.settings.get("DB_FILE_NAME")
        )
    
    def open_spider(self, spider):
        self.connection = connect(self.file_name)

    def process_item(self, item, spider):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO videocard (name, price, link) VALUES (?, ?, ?)", [item["name"], item["price"], item ["link"]])
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()
