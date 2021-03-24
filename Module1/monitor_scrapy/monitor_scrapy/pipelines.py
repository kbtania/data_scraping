# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlite3 import connect
from scrapy.exceptions import DropItem


class MonitorScrapyPipeline:
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
        cursor.execute("SELECT COUNT(*) FROM monitor WHERE model = ?", [item["model"]])
        if cursor.fetchone()[0] > 0:
            raise DropItem(f"Duplicate {item['model']}")        
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
        cursor.execute("INSERT INTO monitor (model, screen, matrix, functions, connection_type) VALUES (?, ?, ?, ?, ?)", [item["model"], item["screen"], item ["matrix"], item["functions"], item["connection_type"]])
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()
