# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie20162021Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieInfoItem(scrapy.Item):
    orderNum = scrapy.Field()  # 排名
    movie_id=scrapy.Field()         #电影id
    movie_name=scrapy.Field()       # 电影名
    release_year=scrapy.Field()      # 年份
    director = scrapy.Field()          # 导演
    starring=scrapy.Field()              # 主演
    genre=scrapy.Field()                # 类型
    languages=scrapy.Field()        # 语言
    country=scrapy.Field()            # 国别
    rating_num=scrapy.Field()           # 评分
    vote_num=scrapy.Field()              # 评分人数
    rating_per_stars5=scrapy.Field()    #五星占比
    rating_per_stars4=scrapy.Field()    #四星占比
    rating_per_stars3 = scrapy.Field()  # 三星占比
    rating_per_stars2 = scrapy.Field()  # 二星占比
    rating_per_stars1 = scrapy.Field()  # 一星占比
    comment_num=scrapy.Field()          #短评数