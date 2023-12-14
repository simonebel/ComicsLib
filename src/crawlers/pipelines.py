# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from crawlers.items import AuthorsItem
from sql import crud
from sql.database import SessionLocal, get_db
from sql.schemas import Author
from utils.log import get_log

logger = get_log(__file__)


class CrawlersPipeline:
    def process_item(self, item, spider):
        if isinstance(item, AuthorsItem):
            self.save_author(item)
        return item

    def save_author(self, author_item: AuthorsItem):
        author = Author(**author_item._values)
        author.generate_id()
        with SessionLocal() as db:
            crud.Author.create(db, author)
