#-*- codeing=utf-8 -*-
#@Time:2022/6/3 19:20
#@Author:王钰娜
#@File : test2016_2021.py
#@Software:PyCharm

#爬取2016-2021年年度榜单

import re
import os
import requests
import pandas as pd
import time
import random
from lxml import etree
from requests import exceptions

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.4153 SLBChan/103',
'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; _ga=GA1.2.427673604.1636166384; _gid=GA1.2.746917562.1654249482; __gpi=UID=00000560be867817:T=1652757447:RT=1654258073:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1654269639; __utmz=30149280.1654271929.15.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1654271929.13.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ct=y; dbcl2="257056199:i29dO0yQnj0"; ck=UGyB; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654310750%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.14.1654310750.1654276365.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.427673604.1636166384.1654271929.1654310750.16; __utma=223695111.891526106.1636166384.1654271929.1654310750.14; __utmb=223695111.0.10.1654310750; __utmt=1; __utmb=30149280.3.9.1654310898321'
}


# url='https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&year_range=2021,2021'
# response=requests.get(url,headers=headers)
# result=response.json()
# datalists=result['data']
#
# host_movies_id_and_title = {}
# for data in datalists:
#             movie_id = data['id']  # 电影Id
#             movie_name = data['title']  # 电影名
#             host_movies_id_and_title[movie_id] =movie_name
# sum=1
# for mid, mtitle in host_movies_id_and_title.items():
#     print( ' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + mtitle + ' )')
#     sum += 1

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_hot_movies_id(movie_sum,year):

    url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}&year_range='+year+","+year
    print('====================>> Start time: ' + get_current_time() + ' <<====================')
    print('========================>> 共' + str(movie_sum) + ' 部影片 <<========================')
    host_movies_id_and_title={}
    for i in range(0, movie_sum, 20):
        hot_page_url = url.format(i)
        sleepTime = random.randint(1, 5)
        time.sleep(sleepTime)
        try:
            response = requests.get(hot_page_url,headers=headers)
            result = response.json()['data']  # type: list
            response.close()
        except Exception as e:
            print(get_current_time() + '===========>> 正在重试...')
            response = requests.get(hot_page_url, headers=headers)
            result = response.json()['data']  # type: list
            response.close()

        for each_movie in result:
            host_movies_id_and_title[each_movie['id']] = each_movie['title']
            #print(host_movies_id_and_title)

    sum = 1
    for mid, mtitle in host_movies_id_and_title.items():
            print(' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + mtitle + ' )')
            sum += 1
    return host_movies_id_and_title

def get_source_page(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    sleepTime=random.randint(1,5)
    time.sleep(sleepTime)

    timeout = 20

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

    # header = {
    #     'User-agent': random.choice(UserAgent_List),
    #     'Host': 'movie.douban.com',
    #     #'Referer': 'https://movie.douban.com/subject/24773958/?from=showing',
    # }
    cookies = {
        'll': '"108296"',
        'bid': 'MRDv7XK7ulc',
        '__gads': 'ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg',
        'douban-fav-remind': '1',
        'viewed': '"35863422"',
        'gr_user_id': 'c13926ad-b2bf-4523-bcaf-5e328e8093d7',
        '__utmc': '30149280',
        '__utmc': '223695111',
        '_vwo_uuid_v2': 'D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211',
        'Hm_lvt_16a14f3002af32bf3a75dfe352478639': '1654181834',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        '__yadk_uid': 'VBD2gPlIToXExQUHrPzYmVL6VPogQZIz',
        '__utmv': '30149280.25705',
        '_ga': 'GA1.2.427673604.1636166384',
        '_gid': 'GA1.2.746917562.1654249482',
        'Hm_lpvt_16a14f3002af32bf3a75dfe352478639': '1654269639',
        '__utmz': '30149280.1654271929.15.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        '__utmz': '223695111.1654271929.13.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'ct': 'y',
        'dbcl2': '"257056199:i29dO0yQnj0"',
        'ck': 'UGyB',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1654310750%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D',
        '_pk_ses.100001.4cf6': '*',
        'ap_v': '0,6.0',
        '__utma': '30149280.427673604.1636166384.1654271929.1654310750.16',
        '__utma': '223695111.891526106.1636166384.1654271929.1654310750.14',
        '__utmb': '223695111.0.10.1654310750',
        '__gpi': 'UID=00000560be867817:T=1652757447:RT=1654311170:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ',
        '__utmt': '1',
        '__utmb': '30149280.6.9.1654311643377',
        '_pk_id.100001.4cf6': '04e032174f9c4f20.1636166383.14.1654311647.1654276365.',
    }

    header = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="8"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-agent': random.choice(UserAgent_List),
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://movie.douban.com/tag/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; _ga=GA1.2.427673604.1636166384; _gid=GA1.2.746917562.1654249482; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1654269639; __utmz=30149280.1654271929.15.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1654271929.13.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ct=y; dbcl2="257056199:i29dO0yQnj0"; ck=UGyB; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654310750%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fexplore%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.427673604.1636166384.1654271929.1654310750.16; __utma=223695111.891526106.1636166384.1654271929.1654310750.14; __utmb=223695111.0.10.1654310750; __gpi=UID=00000560be867817:T=1652757447:RT=1654311170:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; __utmt=1; __utmb=30149280.6.9.1654311643377; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.14.1654311647.1654276365.',
    }

    # time.sleep(random.randint(5, 15))
    # response = requests.get(url, headers=header, proxies=proxies, cookies=cookie_nologin, timeout=timeout)
    try:
        response = requests.get(url, headers=header, cookies=cookies, timeout=timeout,verify=False)
    except exceptions.Timeout as e:
        print('请求超时, 正在重试...', e)
        response = requests.get(url, headers=header,  cookies=cookies, timeout=timeout, verify=False)
        #response = None
    except exceptions.ProxyError as e:
        print('代理错误, 正在更换代理...', e)
        response = None
    return response

def get_movie_info(eachMovie):
    movie_info = []
    # movie_id = movie_id
    movie_name = eachMovie.xpath('//span[@property="v:itemreviewed"]/text()')[0]    #电影名
    movie_name.replace(',', ' ')  # 名称里面可能含有","，转换为csv时可能出错
    release_year = eachMovie.xpath('//span[@class="year"]/text()')[0].strip('()')   #年份
    director = eachMovie.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')[0]    #导演
    starring = eachMovie.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()')  #主演
    starring = "/".join(starring)
    genre = eachMovie.xpath('//span[@property="v:genre"]/text()')   #类型
    genre = "/".join(genre)
    info = eachMovie.xpath('//div[@id="info"]//text()')
    for i in range(0, len(info)):
        if str(info[i]).find('语言') != -1:
            languages = info[i + 1].strip() #语言
        if str(info[i]).find('制片国家') != -1:
            country = info[i + 1].strip()   #国别
    country = country
    languages = languages
    rating_num = eachMovie.xpath('//strong[@property="v:average"]/text()')[0]   #评分
    vote_num = eachMovie.xpath('//span[@property="v:votes"]/text()')[0]         #评分人数
    rating_per_stars5 = eachMovie.xpath('//span[@class="rating_per"]/text()')[0]    #五星占比,四星占比,三星占比,二星占比,一星占比
    rating_per_stars4 = eachMovie.xpath('//span[@class="rating_per"]/text()')[1]
    rating_per_stars3 = eachMovie.xpath('//span[@class="rating_per"]/text()')[2]
    rating_per_stars2 = eachMovie.xpath('//span[@class="rating_per"]/text()')[3]
    rating_per_stars1 = eachMovie.xpath('//span[@class="rating_per"]/text()')[4]
    introduction = eachMovie.xpath('//span[@property="v:summary"]/text()')[0].strip()   #简介
    comment_num = eachMovie.xpath('//div[@id="comments-section"]/div[@class="mod-hd"]/h2//a/text()')[0] #短评数
    comment_num = re.findall('\d+', comment_num)[0]
    movie_info.extend([movie_name, release_year, director, starring, genre, country, languages,
                       rating_num, vote_num, rating_per_stars5, rating_per_stars4, rating_per_stars3,
                       rating_per_stars2, rating_per_stars1, comment_num, introduction])
    return movie_info

def start_spider_movies_info(movies_id_and_title_dict,year):
    """
    指定需要爬取的影片
    :param movies_id_and_title_dict:
    :return:
    """

    all_movie_urls = ['https://movie.douban.com/subject/{}/'.format(k) for k, v in movies_id_and_title_dict.items()]
    movies_all = []
    sum = 1
    for each_page in all_movie_urls:
        movie_id = each_page.split('/')[-2]
        print(get_current_time() + ' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + movies_id_and_title_dict[movie_id] + ' )')
        sum += 1
        try:
            html = get_source_page(each_page)
            selector = etree.HTML(html.text)
            movies_all.append(get_movie_info(selector))
            html.close()
        except Exception as e:
            print(e)
            print(get_current_time()+ "------> 爬取失败, 正在跳过...")
            continue
    data = pd.DataFrame(movies_all)
    filename = 'moveie_'+year+'_top500_1.csv'
    number = 1
    if number == 1:
        info_headers = ['名称', '年份', '导演', '演员', '类型', '国别', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比',
                        '二星占比', '一星占比', '短评数', '简介']
        data.to_csv(filename, header=info_headers, index=False, mode='a+', encoding="utf-8-sig")
        number += 1
    else:
        data.to_csv(filename, header=False, index=False, mode='a+', encoding="utf-8-sig")

    data = []
    print('====================>> Finsh time: ' + get_current_time() + ' <<====================')

if __name__ == '__main__':
    movie_sum=50
    year='2020'
    movies_id_and_title=get_hot_movies_id(movie_sum,year)

    #获取电影详情
    start_spider_movies_info(movies_id_and_title,year)
