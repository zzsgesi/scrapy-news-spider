# Define your item pipelines here
# scrapy crawl news
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WangyiPipeline:
    def open_spider(self, spider):
        self.f=open("./网易新闻.csv",'a',encoding='utf-8')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write(f'{item["title"]}\n,{item["publish_time"]}\n,{item["writer"]}\n,{item["content"]}\n,{item["new_url"]}\n')
        return item
