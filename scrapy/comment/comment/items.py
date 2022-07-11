# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    title=scrapy.Field() #电影名
    user=scrapy.Field() #用户
    watched=scrapy.Field()  #是否看过
    rating=scrapy.Field()   ## 五星评分
    comment_time=scrapy.Field() #评论时间
    votes=scrapy.Field()        #有用数
    content=scrapy.Field()      #评论内容
