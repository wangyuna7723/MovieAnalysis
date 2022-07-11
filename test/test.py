#-*- codeing=utf-8 -*-
#@Time:2022/5/28 15:58
#@Author:王钰娜
#@File : test3.py
#@Software:PyCharm

import re
import os
import requests
import pandas as pd
import time
import random
from lxml import etree
from requests import exceptions
from requests.adapters import HTTPAdapter


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_source_page(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    timeout = 5

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
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]

    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/explore',
        #'Cookie':'bid=KVMeTcXg6Is; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1653988963%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsvL9QhXmH8L2sBoYzxlfvfLZqi_bugiZ3wn-lIxs_lb96gHdqAWhscyYnkk8TELc%26wd%3D%26eqid%3D8adaf828000008f9000000066291d3fb%22%5D; _pk_id.100001.4cf6=05d44d250d94acab.1652664374.8.1653988963.1653836682.; __utma=30149280.245170381.1652664376.1653743533.1653836684.9; __utmz=30149280.1653724282.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1300725694.1652664376.1653743533.1653836684.…I_MZcH2JpZ0VzckzcAruohBBlOiQu2g; ll="108296"; _vwo_uuid_v2=D8E67C61003D52279199379B4029B92DB|dd9240d48301ee76c152fb6037da6d10; ct=y; __gpi=UID=00000582c1b669af:T=1652807673:RT=1653724303:S=ALNI_MazZDAryvzrWiy9Lo198GxnJYlh8w; douban-fav-remind=1; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1652808343; dbcl2="257056199:UGJSp+dubHg"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25705; ck=fWPs; __utmc=30149280; __utmc=223695111; __yadk_uid=fnsY9u2qCOE3slz4IA9rt3w8RTuPfE6v; _pk_ses.100001.4cf6=*; ap_v=0,6.0'
    }

    # 代理IP
    proxies = {
        'http:': 'http://121.232.146.184',
        'https:': 'https://144.255.48.197',
        # 'https:': "https://175.9.77.240:80",
        # 'https:':"https://119.5.177.167:4386",
        # 'https:':"https://210.26.54.43:808",
    }

    session = requests.Session()

    cookies = {
        'bid': 'KVMeTcXg6Is',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1653988963%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsvL9QhXmH8L2sBoYzxlfvfLZqi_bugiZ3wn-lIxs_lb96gHdqAWhscyYnkk8TELc%26wd%3D%26eqid%3D8adaf828000008f9000000066291d3fb%22%5D',
        '_pk_id.100001.4cf6': '05d44d250d94acab.1652664374.8.1653988963.1653836682.',
        '__utma': '30149280.245170381.1652664376.1653743533.1653836684.9',
        '__utmz': '30149280.1653724282.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        '__utma': '223695111.1300725694.1652664376.1653743533.1653836684.7',
        '__utmz': '223695111.1653724282.4.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        '__gads': 'ID=a8a67c9d965bfafd-22f00cad2fd3004f:T=1652664377:RT=1652664377:S=ALNI_MZcH2JpZ0VzckzcAruohBBlOiQu2g',
        'll': '"108296"',
        '_vwo_uuid_v2': 'D8E67C61003D52279199379B4029B92DB|dd9240d48301ee76c152fb6037da6d10',
        'ct': 'y',
        '__gpi': 'UID=00000582c1b669af:T=1652807673:RT=1653724303:S=ALNI_MazZDAryvzrWiy9Lo198GxnJYlh8w',
        'douban-fav-remind': '1',
        'Hm_lvt_16a14f3002af32bf3a75dfe352478639': '1652808343',
        'dbcl2': '"257056199:UGJSp+dubHg"',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        '__utmv': '30149280.25705',
        'ck': 'fWPs',
        '__utmc': '30149280',
        '__utmc': '223695111',
        '__yadk_uid': 'fnsY9u2qCOE3slz4IA9rt3w8RTuPfE6v',
        '_pk_ses.100001.4cf6': '*',
        'ap_v': '0,6.0',
    }

    time.sleep(random.randint(1, 5))
    # response = requests.get(url, headers=header, proxies=proxies, cookies=cookie_nologin, timeout=timeout)
    try:
        response = requests.get(url, headers=header,cookies=cookies, proxies=proxies,timeout=timeout)
    except Exception as e:
        print(' 正在跳过...', e)
        response = None
    return response


def get_hot_movies_id(movie_sum, movie_tag):
    """
    获取影片名和影片ID
    :param movie_sum: 指定爬取电影的数量，范围 1~500
    :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
    :return:
    """
    movie_tags = {'热门': '%E7%83%AD%E9%97%A8', '豆瓣高分': '%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86'}
    tag = movie_tags[movie_tag]
    print('====================>> Start time: ' + get_current_time() + ' <<====================')
    print('========================>> 共' + str(movie_sum) + ' 部影片 <<========================')
    host_movies_id_and_title = {}
    for i in range(0,movie_sum,20):
        hot_page_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + tag + '&sort=recommend' \
                        '&page_limit=20' + '&page_start='+str(i)
        try:
            response = get_source_page(hot_page_url)
            result=response.json()['subjects']  # type: list
            response.close()
        except Exception as e:
            print(get_current_time() + '===========>> 正在重试...')
            response = get_source_page(hot_page_url).json()['subjects']  # type: list
        print("====================第"+str(i//20+1)+"页====================")

        for each_movie in result:
            host_movies_id_and_title[each_movie['id']] = each_movie['title']
        # print(host_movies_id_and_title)

        for mid, mtitle in host_movies_id_and_title.items():
            print(mid + ' --> ' + mtitle)
    return host_movies_id_and_title


def start_spider_movies_info(movies_id_and_title_dict):
    """
    指定需要爬取的影片
    :param movies_id_and_title_dict:
    :return:
    """

    all_movie_urls = ['https://movie.douban.com/subject/{}'.format(k) for k, v in movies_id_and_title_dict.items()]
    movies_all = []
    sum = 1
    for each_page in all_movie_urls:
        movie_id = each_page.split('/')[-1]
        print(get_current_time() + ' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + movies_id_and_title_dict[movie_id] + ' )')
        sum += 1
        try:
            html = get_source_page(each_page)

        except Exception as e:
            print(e)
            print(get_current_time() + "------> 爬取失败, 正在重试...")
            html = get_source_page(each_page)
            print("正在跳过.....")
            continue
        selector = etree.HTML(html.text)
        html.close()
        #print(html.text)
        movies_all.append(get_movie_info(selector))
    data = pd.DataFrame(movies_all)
    filename = 'movie_info_top500.csv'
    number = 1
    if number == 1:
        info_headers = ['名称', '年份', '导演', '演员', '类型', '国别', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比',
                        '二星占比', '一星占比', '短评数', '简介']
        data.to_csv(filename, header=info_headers, index=False, mode='a+', encoding="utf-8")
        number += 1
    else:
        data.to_csv(filename, header=False, index=False, mode='a+', encoding="utf-8")

    data = []
    print('====================>> Finsh time: ' + get_current_time() + ' <<====================')


def start_spider_comment(movies_id_and_title_dict):
    """
    指定需要爬取影评的影片
    :param movies_id_and_title_dict:
    :return:
    """
    #爬取前5部影片的影评
    movies_id_and_title_dict=movies_id_and_title_dict[0:5]
    if not os.path.exists('../comment_data'):
        os.mkdir('../comment_data')
        print("所有影评以片名名命保存在 comment_data 文件夹下...")
    number = 1
    for movie_id, movie_name in movies_id_and_title_dict.items():
        print(get_current_time() + ' ----->> 正在爬取第 ' + str(number) + '部影片( ' + movie_name + ' )')
        get_comment_info_to_cvs(movie_id, movie_name)
        # get_comment_info_to_txt(movie_id, movie_name)
        number += 1
    print('====================>> Finsh time: ' + get_current_time() + ' <<====================')


def get_comments(eachComment):
    commentlist = []
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
    content = eachComment.xpath("./p/span/text()")[0]  # 评论内容

    commentlist.append(user)
    commentlist.append(watched)
    commentlist.append(rating)
    commentlist.append(comment_time)
    commentlist.append(votes)
    commentlist.append(content.strip())
    print(commentlist)
    return commentlist


def get_movie_info(eachMovie):
    movie_info = []
    # movie_id = movie_id
    movie_name = eachMovie.xpath('//span[@property="v:itemreviewed"]/text()')[0]    #电影名
    release_year = eachMovie.xpath('//span[@class="year"]/text()')[0].strip('()')   #年份
    director = eachMovie.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')[0]    #导演
    starring = eachMovie.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()')         #主演
    starring = ",".join(starring)
    genre = eachMovie.xpath('//span[@property="v:genre"]/text()')   #类型
    genre = ",".join(genre)
    info = eachMovie.xpath('//div[@id="info"]//text()')
    for i in range(0, len(info)):
        if str(info[i]).find('语言') != -1:
            languages = info[i + 1].replace(' / ', ',').strip()     #语言
        if str(info[i]).find('制片国家') != -1:
            country = info[i + 1].replace(' / ', ',').strip()       #国别
    country = country
    languages = languages
    rating_num = eachMovie.xpath('//strong[@property="v:average"]/text()')[0]   #评分
    vote_num = eachMovie.xpath('//span[@property="v:votes"]/text()')[0]            #评分人数
    rating_per_stars5 = eachMovie.xpath('//span[@class="rating_per"]/text()')[0]    #五星占比,四星占比,三星占比,二星占比,一星占比
    rating_per_stars4 = eachMovie.xpath('//span[@class="rating_per"]/text()')[1]
    rating_per_stars3 = eachMovie.xpath('//span[@class="rating_per"]/text()')[2]
    rating_per_stars2 = eachMovie.xpath('//span[@class="rating_per"]/text()')[3]
    rating_per_stars1 = eachMovie.xpath('//span[@class="rating_per"]/text()')[4]
    introduction = eachMovie.xpath('//span[@property="v:summary"]/text()')[0].strip()   #简介
    comment_num = eachMovie.xpath('//div[@id="comments-section"]/div[@class="mod-hd"]/h2//a/text()')[0]  #短评数
    comment_num = re.findall('\d+', comment_num)[0]
    movie_info.extend([movie_name, release_year, director, starring, genre, country, languages,
                       rating_num, vote_num, rating_per_stars5, rating_per_stars4, rating_per_stars3,
                       rating_per_stars2, rating_per_stars1, comment_num, introduction])
    return movie_info


def get_comment_info_to_txt(movie_id, movie_name):
    """
    爬取指定影片的短评并写入txt文件（文件以影片名命名）
    :param movie_id:
    :param movie_name:
    :return:
    """
    base_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/comments?start='
    all_page_comments = [base_url + '{}'.format(x) for x in range(0, 201, 20)]
    filename = movie_name + '.txt'
    filepath = os.path.join('../comment_data', filename)
    for each_page in all_page_comments:
        try:
            html = get_source_page(each_page)
            selector = etree.HTML(html.text)
            comments = selector.xpath("//div[@class='comment']")
            comments_all = []
            for each in comments:
                # comments_all.append(get_comments(each))
                each_comment = get_comments(each)
                with open(filepath, 'a', encoding='utf-8') as f:
                    # f.write(movie_name + '->' + str(movie_id) + '\n')
                    f.write(each_comment[0] + "\t" + each_comment[1] + "\t" + each_comment[2] + "\t" + each_comment[3] \
                            + "\t" + each_comment[4] + "\t" + each_comment[5] + "\n")
        except:
            # print('跳过一个页面')
            continue


def get_comment_info_to_cvs(movie_id, movie_name):
    """
    爬取指定影片的短评并写入csv文件（文件以影片名命名）
    :param movie_id:
    :param movie_name:
    :return:
    """
    base_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/comments?start={}&limit=20&status=P&sort=new_score'
    all_page_comments = [base_url .format(x) for x in range(0, 201, 20)]
    filename = movie_name + '.csv'
    filepath = os.path.join('../comment_data2', filename)
    number = 1
    for each_page in all_page_comments:
        try:
            html = get_source_page(each_page)
            selector = etree.HTML(html.text)
            #print(html.text)
            comments = selector.xpath("//div[@class='comment']")
            comments_all = []
            for each in comments:
                comments_all.append(get_comments(each))
            data = pd.DataFrame(comments_all)
            # 写入csv文件
            try:
                if number == 1:
                    csv_headers = ['用户', '是否看过', '评分', '评论时间', '有用数', '评论']
                    data.to_csv(filepath, header=csv_headers, index=False, mode='a+', encoding="utf-8")
                    number += 1
                else:
                    data.to_csv(filepath, header=False, index=False, mode='a+', encoding="utf-8")
            except UnicodeEncodeError:
                print("编码错误, 跳过...")
            data = []
        except:
            print('跳过一个页面')
            continue


if __name__ == '__main__':
    ## 使用请取消注释 -> 爬取影片信息
    movies_id_and_title = get_hot_movies_id(500, '豆瓣高分')


    ## 使用请取消注释 -> 爬取影评
    # movies_id_and_title = get_hot_movies_id(100, '豆瓣高分')
    """
    :param movie_sum: 指定爬取电影的数量，范围 1~100
    :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
    """
    start_spider_movies_info(movies_id_and_title)
    start_spider_comment(movies_id_and_title)


    """
    :param movie_sum: 指定爬取电影的数量，范围 1~500
    :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
    """




