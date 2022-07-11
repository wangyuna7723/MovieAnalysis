#-*- codeing=utf-8 -*-
#@Time:2022/6/11 16:45
#@Author:王钰娜
#@File : MovieComment.py
#@Software:PyCharm

import scrapy
import random
import time
from scrapy import Request
from ..items import CommentItem
from lxml import etree

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

class MovieCommentSpider(scrapy.Spider):
    name = "MovieComment"
    allowed_domains = ["movie.douban.com"]
    movies_id_and_title_dict = {'25662329': '疯狂动物城 Zootopia', '26387939': '摔跤吧！爸爸 Dangal',
                           '26580232': '看不见的客人 Contratiempo',
                           '25986180': '釜山行 부산행', '26325320': '血战钢锯岭 Hacksaw Ridge',
                           '25980443': '海边的曼彻斯特 Manchester by the Sea'}
    # movies_id_and_title_dict={'26387939': '摔跤吧！爸爸 Dangal Test'}

    # 设置起始链接
    def start_requests(self):
        number = 1
        for movie_id, movie_name in self.movies_id_and_title_dict.items():
            print(' ----->> 正在爬取第 ' + str(number) + '部影片( ' + movie_name + ' )')
            base_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/comments?start={}&limit=20&status=P&sort=new_score'
            number += 1
            all_page_comments = [base_url.format(x) for x in range(0, 201, 20)]

            for each_page in all_page_comments:

                item=CommentItem()
                item['title']=movie_name
                time.sleep(random.randint(1,10))
                yield Request(url=each_page,meta={"item":item},callback=self.getComment,headers=headers)


    #得到电影评论
    def getComment(self,response):
        html = response
        selector = etree.HTML(html.text)
        comments = selector.xpath("//div[@class='comment']")
        for eachComment in comments:

            user = eachComment.xpath("./h3/span[@class='comment-info']/a/text()")[0]  # 用户
            watched = eachComment.xpath("./h3/span[@class='comment-info']/span[1]/text()")[0]  # 是否看过
            rating = eachComment.xpath("./h3/span[@class='comment-info']/span[2]/@title")  # 五星评分
            if len(rating) > 0:
                rating = rating[0]

            comment_time = eachComment.xpath("./h3/span[@class='comment-info']/span[3]/@title")  # 评论时间
            if len(comment_time) > 0:
                comment_time = comment_time[0]
            else:
                comment_time = ' '

            votes = eachComment.xpath("./h3/span[@class='comment-vote']/span/text()")[0]  # "有用"数
            content = eachComment.xpath("./p/span/text()")[0].strip()  # 评论内容

            item= response.meta["item"]
            item['user']=user
            item['watched']=watched
            item['rating']=rating
            item['votes'] = votes
            item['comment_time'] = comment_time
            item['content'] = content
            yield item
