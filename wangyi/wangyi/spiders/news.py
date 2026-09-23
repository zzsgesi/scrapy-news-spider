import scrapy
from wangyi.items import WangyiItem
# scrapy crawl news

class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = ["http://news.163.com/"]

    def parse(self, resp,**kwargs):
        hrefs=resp.xpath('//*[@class="hidden"]/div/a/@href').extract()
        for href in hrefs:
            if "photoview" in href or "photo" in href or "video" in href or "caozhi" in href:
                continue
            yield scrapy.Request(
                url=href,
                method='get',
                callback=self.parse_detail)

    def parse_detail(self, resp, **kwargs):
        title=resp.xpath('//title/text()').extract_first()
        publish_time_1=resp.xpath('/html/@data-publishtime').extract_first()
        publish_time_2=resp.xpath('//*[@id="ptime"]/text()').extract_first()
        publish_time_3=resp.xpath('//*[@class="pub_time"]/text()').extract_first()
        if publish_time_1:
            publish_time=publish_time_1
        elif publish_time_2:
            publish_time=publish_time_2
        else:
            publish_time=publish_time_3
        writer_1=resp.xpath('//*[@class="post_info"]/a[1]/text()').extract_first()
        writer_2=resp.xpath('//*[@rel="nofollow"]/text()').extract_first()
        writer_3=resp.xpath('//*[@class="post_info"]/text()').extract_first()
        if writer_1 is None:
            writer=writer_2
        elif writer_1=="举报":
            writer=writer_3.rsplit(': ',)[1].strip()
        else:
            writer=writer_1
        content_list=resp.xpath('//*[@class="post_body"]/p/text()').extract()
        content=''.join(content_list)
        wangyi=WangyiItem()
        wangyi['title']=title
        wangyi['publish_time']=publish_time
        wangyi['writer']=writer
        wangyi['content']=content
        wangyi['new_url']=resp.url
        yield wangyi


