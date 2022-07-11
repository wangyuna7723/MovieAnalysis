# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import MovieInfoItem

class DoubanmoviePipeline:
    def process_item(self, item, spider):
        return item

class MovieInfoCSVPipeline:
    file=None
    index_top=0 #第几行
    index_comment = 0  # 第几行

    def process_item(self, item, spider):#爬虫每次运行时，会执行这个函数
        #把item保存到csv
        if type(item) == MovieInfoItem:
            # 以追加的形式打开
            self.file = open("movie_info_top500_7.csv", "a", encoding="utf-8-sig")
            if self.index_top==0:
                #写表头
                column_name="排名,电影id,名称, 年份, 导演, 演员, 类型, 国别, 语言, 评分, 评分人数, 五星占比, 四星占比, 三星占比,二星占比, 一星占比, 简介,短评数"+"\n"
                self.file.write(column_name)
                self.index_top=1

            movieInfo_str=str(item["orderNum"])+","+str(item["movie_id"])+","+str(item["movie_name"])+","+str(item["release_year"])+","+str(item["director"])+","+str(item["starring"])+","+str(item["genre"])+","+str(item["languages"])+","+str(item["country"])+","+str(item["rating_num"] )+ ","+str(item["vote_num"])+","+str(item["rating_per_stars5"])+","+str(item["rating_per_stars4"])+","+str(item["rating_per_stars3"])+","+str(item["rating_per_stars2"])+","+str(item["rating_per_stars1"])+","+str(item["introduction"])+","+str(item["comment_num"])+"\n"

            self.file.write(movieInfo_str)

        return item
    def close_spider(self,spider):#爬虫结束时，执行
        self.file.close()
