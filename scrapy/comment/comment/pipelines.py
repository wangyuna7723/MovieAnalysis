# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CommentPipeline:
    file = None
    index_top = 0  # 第几行
    index_comment = 0  # 第几行

    def process_item(self, item, spider):
        # 以追加的形式打开
        self.file = open(item['title']+".csv", "a", encoding="utf-8-sig")
        if self.index_top == 0:
            # 写表头
            column_name = "用户,是否看过,评分,评论时间,有用数,评论" + "\n"
            self.file.write(column_name)
            self.index_top = 1

        movieInfo_str = str(item["user"]) + "," + str(item["watched"]) + "," + str(item["rating"]) + "," + str(item["comment_time"]) + "," + str(item["votes"]) + "," + str(item["content"]) + "\n"

        self.file.write(movieInfo_str)
        return item

    def close_spider(self,spider):#爬虫结束时，执行
        self.file.close()