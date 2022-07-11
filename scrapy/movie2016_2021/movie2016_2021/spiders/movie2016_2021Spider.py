#-*- codeing=utf-8 -*-
#@Time:2022/6/4 12:32
#@Author:王钰娜
#@File : movie2016_2021Spider.py
#@Software:PyCharm
import scrapy
from scrapy import Request
import time
import  re
import random
import requests
from lxml import etree
from requests import exceptions
from ..items import MovieInfoItem

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
]

header = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="8"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-agent': random.choice(UserAgent_List),
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    #'Referer': 'https://movie.douban.com/explore',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1654182386; __utmz=30149280.1654192305.8.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/explore; __utmz=223695111.1654192441.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; dbcl2="257056199:UGJSp+dubHg"; ck=fWPs; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; __gpi=UID=00000560be867817:T=1652757447:RT=1654233167:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654243676%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.8.1654243676.1654237095.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.427673604.1636166384.1654233162.1654243679.10; __utmb=30149280.0.10.1654243679; __utma=223695111.891526106.1636166384.1654233162.1654243679.8; __utmb=223695111.0.10.1654243679',
}

headers={
 'User-agent': random.choice(UserAgent_List),
  'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; _ga=GA1.2.427673604.1636166384; ct=y; __utmz=30149280.1654429190.26.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utmz=223695111.1654429190.24.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __gpi=UID=00000560be867817:T=1652757447:RT=1654429246:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; __utma=30149280.427673604.1636166384.1654429190.1654432432.27; __utmb=30149280.0.10.1654432432; __utmb=223695111.0.10.1654432432; __utma=223695111.891526106.1636166384.1654429190.1654432432.25; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654432432%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DV5Rz6uRyePDZknSyXFRTm3f-OfhyJOcKpWPlDrMwwkccBuEwpg_rI8oObzUenA1M%26wd%3D%26eqid%3De1756268000412ed00000006629c9603%22%5D; _pk_ses.100001.4cf6=*; dbcl2="257672707:NFk1zpjKEMo"; ck=XAJD; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.24.1654434597.1654429305.'}
cookies = {
    'll': '"108296"',
    'bid': 'MRDv7XK7ulc',
    '__gads': 'ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg',
    'douban-fav-remind': '1',
    'viewed': '"35863422"',
    'gr_user_id': 'c13926ad-b2bf-4523-bcaf-5e328e8093d7',
    '_vwo_uuid_v2': 'D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211',
    'Hm_lvt_16a14f3002af32bf3a75dfe352478639': '1654181834',
    'push_noty_num': '0',
    'push_doumail_num': '0',
    '__yadk_uid': 'VBD2gPlIToXExQUHrPzYmVL6VPogQZIz',
    '__utmv': '30149280.25705',
    '_ga': 'GA1.2.427673604.1636166384',
    'ct': 'y',
    '__utmz': '30149280.1654429190.26.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    '__utmc': '30149280',
    '__utmz': '223695111.1654429190.24.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    '__utmc': '223695111',
    '__gpi': 'UID=00000560be867817:T=1652757447:RT=1654429246:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ',
    '__utma': '30149280.427673604.1636166384.1654429190.1654432432.27',
    '__utmb': '30149280.0.10.1654432432',
    '__utma': '223695111.891526106.1636166384.1654429190.1654432432.25',
    '__utmb': '223695111.0.10.1654432432',
    'ap_v': '0,6.0',
    '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1654432432%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DV5Rz6uRyePDZknSyXFRTm3f-OfhyJOcKpWPlDrMwwkccBuEwpg_rI8oObzUenA1M%26wd%3D%26eqid%3De1756268000412ed00000006629c9603%22%5D',
    '_pk_ses.100001.4cf6': '*',
    'dbcl2': '"257672707:NFk1zpjKEMo"',
    'ck': 'XAJD',
    '_pk_id.100001.4cf6': '04e032174f9c4f20.1636166383.24.1654434431.1654429305.',
}


timeout = 20


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_source_page(url):
        sleepTime = random.randint(1, 5)
        time.sleep(sleepTime)
        try:
            response = requests.get(url, headers=header, cookies=cookies, timeout=timeout,
                                    verify=False)
        except exceptions.Timeout as e:
            print('请求超时, 正在重试...', e)
            response = requests.get(url, headers=header, cookies=cookies, timeout=timeout,
                                    verify=False)
            # response = None
        except exceptions.ProxyError as e:
            print('代理错误, 正在更换代理...', e)
            response = None
        return response

class MovieSpider(scrapy.Spider):
    name = 'movie2016_2021'
    allowed_domains = ["movie.douban.com"]
    movie_sum = 20  #电影数
    year=""         #当前爬取的年份

    movies_id_and_title_dict = {}


    #设置起始链接
    def start_requests(self):
        """
        获取影片名和影片ID
        :param movie_sum: 指定爬取电影的数量，范围 1~500
        :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
        :return:
        """
        print('====================>> Start time: ' + get_current_time() + ' <<====================')
        print('========================>> 共' + str(self.movie_sum) + ' 部影片 <<========================')
        years = [2021]
        #, 2017, 2018, 2019, 2020, 2021
        for j in years:
            self.year = str(j)
            self.movies_id_and_title_dict={}
            for i in range(0, self.movie_sum, 20):
                sleepTime = random.randint(1, 5)
                time.sleep(sleepTime)
                hot_page_url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start='+str(i)+'&year_range=' + str(j) + "," + str(j)
                try:
                    response = requests.get(hot_page_url, headers=headers)

                except Exception as e:
                    print(get_current_time() + '===========>> 正在重试...'+e)
                    response = requests.get(hot_page_url, headers=headers)

                result = response.json()['data']  # type: list
                response.close()
                for each_movie in result:
                    self.movies_id_and_title_dict[each_movie['id']] = each_movie['title']
                    # print(host_movies_id_and_title)

                for mid, mtitle in self.movies_id_and_title_dict.items():
                    print(mid + ' --> ' + mtitle)

            # 爬取详细信息
            all_movie_urls = ['https://movie.douban.com/subject/{}/'.format(k) for k, v in self.movies_id_and_title_dict.items()]
            movies_all = []
            sum = 1
            for each_page in all_movie_urls:
                movie_id = each_page.split('/')[-2]
                print(get_current_time() + ' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + self.movies_id_and_title_dict[movie_id] + ' )')

                item = MovieInfoItem()  # 实例化电影详情
                item['orderNum'] = sum # 排名
                item['movie_id'] = movie_id  # 电影id

                sum += 1

                sleepTime = random.randint(1, 10)
                time.sleep(sleepTime)
                yield Request(each_page,headers=header,cookies=cookies,callback=self.get_movie_info,meta={'item':item})

    #爬取详细信息
    def get_movie_info(self,response):

        eachMovie = etree.HTML(response.text)
        movie_info = []
        # movie_id = movie_id
        movie_name = eachMovie.xpath('//span[@property="v:itemreviewed"]/text()')[0]  # 电影名
        movie_name.replace(',',' ') #名称里面可能含有","，转换为csv时可能出错
        release_year = eachMovie.xpath('//span[@class="year"]/text()')[0].strip('()')  # 年份
        director = eachMovie.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')[0]  # 导演
        starring = eachMovie.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()')  # 主演
        starring = "/".join(starring)
        genre = eachMovie.xpath('//span[@property="v:genre"]/text()')  # 类型
        genre = "/".join(genre)
        info = eachMovie.xpath('//div[@id="info"]//text()')
        for i in range(0, len(info)):
            if str(info[i]).find('语言') != -1:
                languages = info[i + 1].strip()  # 语言
            if str(info[i]).find('制片国家') != -1:
                country = info[i + 1].strip()  # 国别
        country = country
        languages = languages
        rating_num = eachMovie.xpath('//strong[@property="v:average"]/text()')[0]  # 评分
        vote_num = eachMovie.xpath('//span[@property="v:votes"]/text()')[0]  # 评分人数
        rating_per_stars5 = eachMovie.xpath('//span[@class="rating_per"]/text()')[0]  # 五星占比,四星占比,三星占比,二星占比,一星占比
        rating_per_stars4 = eachMovie.xpath('//span[@class="rating_per"]/text()')[1]
        rating_per_stars3 = eachMovie.xpath('//span[@class="rating_per"]/text()')[2]
        rating_per_stars2 = eachMovie.xpath('//span[@class="rating_per"]/text()')[3]
        rating_per_stars1 = eachMovie.xpath('//span[@class="rating_per"]/text()')[4]
        comment_num = eachMovie.xpath('//div[@id="comments-section"]/div[@class="mod-hd"]/h2//a/text()')[0]  # 短评数
        comment_num = re.findall('\d+', comment_num)[0]

        item= response.meta["item"]
        item['movie_name']=movie_name
        item['release_year'] = release_year
        item['director'] = director
        item['starring'] = starring
        item['genre'] = genre
        item['languages'] = languages
        item['country']=country
        item['rating_num'] = rating_num
        item['vote_num'] = vote_num
        item['rating_per_stars5'] = rating_per_stars5
        item['rating_per_stars4'] = rating_per_stars4
        item['rating_per_stars3'] = rating_per_stars3
        item['rating_per_stars2'] = rating_per_stars2
        item['rating_per_stars1'] = rating_per_stars1
        item['comment_num'] = comment_num

        yield item