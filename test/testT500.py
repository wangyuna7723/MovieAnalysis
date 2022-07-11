#-*- codeing=utf-8 -*-
#@Time:2022/5/31 18:27
#@Author:王钰娜
#@File : testT500.py
#@Software:PyCharm

import re
import os
import requests
import pandas as pd
import time
import random
from lxml import etree
from requests import exceptions


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_source_page(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    sleepTime=random.randint(1,5)
    time.sleep(sleepTime)


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
        'Referer': 'https://movie.douban.com/explore',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1654182386; __utmz=30149280.1654192305.8.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/explore; __utmz=223695111.1654192441.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; dbcl2="257056199:UGJSp+dubHg"; ck=fWPs; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; __gpi=UID=00000560be867817:T=1652757447:RT=1654233167:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654243676%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.8.1654243676.1654237095.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.427673604.1636166384.1654233162.1654243679.10; __utmb=30149280.0.10.1654243679; __utma=223695111.891526106.1636166384.1654233162.1654243679.8; __utmb=223695111.0.10.1654243679',
    }

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
        'Hm_lpvt_16a14f3002af32bf3a75dfe352478639': '1654182386',
        '__utmz': '30149280.1654192305.8.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/explore',
        '__utmz': '223695111.1654192441.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry',
        'dbcl2': '"257056199:UGJSp+dubHg"',
        'ck': 'fWPs',
        'push_noty_num': '0',
        'push_doumail_num': '0',
        '__yadk_uid': 'VBD2gPlIToXExQUHrPzYmVL6VPogQZIz',
        '__utmv': '30149280.25705',
        '__gpi': 'UID=00000560be867817:T=1652757447:RT=1654233167:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1654243676%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D',
        '_pk_id.100001.4cf6': '04e032174f9c4f20.1636166383.8.1654243676.1654237095.',
        '_pk_ses.100001.4cf6': '*',
        'ap_v': '0,6.0',
        '__utma': '30149280.427673604.1636166384.1654233162.1654243679.10',
        '__utmb': '30149280.0.10.1654243679',
        '__utma': '223695111.891526106.1636166384.1654233162.1654243679.8',
        '__utmb': '223695111.0.10.1654243679',
    }

    timeout = 20

    # time.sleep(random.randint(5, 15))
    # response = requests.get(url, headers=header, proxies=proxies, cookies=cookie_nologin, timeout=timeout)
    try:
        response = requests.get(url, headers=header,cookies=cookies, timeout=timeout,verify=False)
    except exceptions.Timeout as e:
        print('请求超时, 正在重试...', e)
        response = requests.get(url, headers=header, cookies=cookies, timeout=timeout, verify=False)
        #response = None
    except exceptions.ProxyError as e:
        print('代理错误, 正在更换代理...', e)
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
    for i in range(0, movie_sum, 20):
        hot_page_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + tag + '&sort=recommend' \
                    '&page_limit=20' + '&page_start='+str(i)
        try:
            response = get_source_page(hot_page_url)
            result = response.json()['subjects']  # type: list
            response.close()
        except Exception as e:
            print(get_current_time() + '===========>> 正在重试...')
            result = get_source_page(hot_page_url).json()['subjects']  # type: list

        for each_movie in result:
            host_movies_id_and_title[each_movie['id']] = each_movie['title']
            #print(host_movies_id_and_title)

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
            selector = etree.HTML(html.text)
            movies_all.append(get_movie_info(selector))
            html.close()
        except Exception as e:
            print(e)
            print(get_current_time()+ "------> 爬取失败, 正在跳过...")
            continue
    data = pd.DataFrame(movies_all)
    filename = 'moveie_info_top500_4.csv'
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
def Test_start_spider_movies_info(movies_id):
    """
    指定需要爬取的影片
    :param movies_id_and_title_dict:
    :return:
    """

    all_movie_urls = ['https://movie.douban.com/subject/{}/'.format(k) for k in movies_id]
    movies_all = []
    sum = 1
    for each_page in all_movie_urls:
        movie_id = each_page.split('/')[-2]
        print(get_current_time() + ' ----->> 正在爬取第 ' + str(sum) + '部影片()'+each_page)
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
    filename = 'moveie_info_topTest.csv'
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

def start_spider_comment(movies_id_and_title_dict):
    """
    指定需要爬取影评的影片
    :param movies_id_and_title_dict:
    :return:
    """
    #前10的影评
    data = {}
    for i, (k, v) in enumerate(movies_id_and_title_dict.items()):
        data[k] = v
        if i == 10:
            print(data)
            break
    if not os.path.exists('../comment_data4'):
        os.mkdir('../comment_data4')
        print("所有影评以片名名命保存在 comment_data4 文件夹下...")
    number = 1
    for movie_id, movie_name in data.items():
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
    movie_name.replace(',', ' ')  # 名称里面可能含有","，转换为csv时可能出错
    release_year = eachMovie.xpath('//span[@class="year"]/text()')[0].strip('()')   #年份
    director = eachMovie.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')[0]    #导演
    starring = eachMovie.xpath('//span[@class="actor"]//span[@class="attrs"]/a/text()')  #主演
    starring = ",".join(starring)
    genre = eachMovie.xpath('//span[@property="v:genre"]/text()')   #类型
    genre = ",".join(genre)
    info = eachMovie.xpath('//div[@id="info"]//text()')
    for i in range(0, len(info)):
        if str(info[i]).find('语言') != -1:
            languages = info[i + 1].replace(' / ', ',').strip() #语言
        if str(info[i]).find('制片国家') != -1:
            country = info[i + 1].replace(' / ', ',').strip()   #国别
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
    filepath = os.path.join('../comment_data4', filename)
    number = 1
    for each_page in all_page_comments:
        try:
            html = get_source_page(each_page)
            selector = etree.HTML(html.text)
            comments = selector.xpath("//div[@class='comment']")
            comments_all = []
            for each in comments:
                comments_all.append(get_comments(each))
            data = pd.DataFrame(comments_all)
            # 写入csv文件
            try:
                if number == 1:
                    csv_headers = ['用户', '是否看过', '评分', '评论时间', '有用数', '评论']
                    data.to_csv(filepath, header=csv_headers, index=False, mode='a+', encoding="utf-8-sig")
                    number += 1
                else:
                    data.to_csv(filepath, header=False, index=False, mode='a+', encoding="utf-8-sig")
            except UnicodeEncodeError:
                print("编码错误, 跳过...")
            data = []
        except:
            print('跳过一个页面')
            continue


if __name__ == '__main__':
    ## 使用请取消注释 -> 爬取影片信息
    #movies_id_and_title = get_hot_movies_id(500, '豆瓣高分')
    """
    :param movie_sum: 指定爬取电影的数量，范围 1~500
    :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
    """
    dict_id=['26611804','1291579','1293350','26614893','1950148','26654498','4798888']
    Test_start_spider_movies_info(dict_id)



    ## 使用请取消注释 -> 爬取影评
    #movies_id_and_title = get_hot_movies_id(100, '豆瓣高分')
    """
    :param movie_sum: 指定爬取电影的数量，范围 1~100
    :param movie_tag: 指定电影排行tag， 范围 '热门' or '豆瓣高分'
    """
    #start_spider_comment(movies_id_and_title)