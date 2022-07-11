#-*- codeing=utf-8 -*-
#@Time:2022/6/3 19:20
#@Author:王钰娜
#@File : test2016_2021.py
#@Software:PyCharm

#爬取2016-2021年年度榜单

import requests

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.4153 SLBChan/103',
'Cookie': 'll="108296"; bid=MRDv7XK7ulc; __gads=ID=d3fd405ce48d8771-22f67b0095ce0032:T=1636166467:RT=1636166467:S=ALNI_Mb1l38gCpg0uBxLDN_rAtn88z6Gtg; douban-fav-remind=1; viewed="35863422"; gr_user_id=c13926ad-b2bf-4523-bcaf-5e328e8093d7; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D233520F42C23E532780E5DE6C33939F3|df2d5a7a50fa144a227339ea5f160211; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1654181834; __utmz=30149280.1654192305.8.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/explore; __utmz=223695111.1654192441.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; dbcl2="257056199:UGJSp+dubHg"; ck=fWPs; push_noty_num=0; push_doumail_num=0; __yadk_uid=VBD2gPlIToXExQUHrPzYmVL6VPogQZIz; __utmv=30149280.25705; __gpi=UID=00000560be867817:T=1652757447:RT=1654233167:S=ALNI_MYKVXyh6Pa79l9Ja2J3PsSATQu3AQ; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1654247766%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.427673604.1636166384.1654243679.1654248107.11; __utma=223695111.891526106.1636166384.1654243679.1654248107.9; _ga=GA1.2.427673604.1636166384; _gid=GA1.2.746917562.1654249482; _pk_id.100001.4cf6=04e032174f9c4f20.1636166383.9.1654250807.1654244057.; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1654250807'
}


url='https://movie.douban.com/ithil_j/activity/movie_annual2021?with_widgets=1&ck=fWPs'
response=requests.get(url,headers=headers)
result=response.json()  ##如果是json数据，直接可以调用json方法
datalists=(result['res']['widgets'])

host_movies_id_and_title = {}
for data in datalists:
    if ' A,B 榜' in data['kind_cn']:
        bang = data['payload']['title']  # 榜单名称
        print(bang)
        items = data['subjects']
        for item in items:
            movie_id = item['id']  # 电影Id
            movie_name = item['title']  # 电影名
            # director=item['info'].split('/')[0] #导演
            # starring=item['info'].split('/')[1:]    #主演
            # country=item['description']     #国别
            # rating_num=item['rating']       #评分
            # playable=item['playable']       #是否上映
            # vote_num=item['rating_count']            #评分人数
            host_movies_id_and_title[movie_id] = movie_name + " " + bang

    if ('C 榜') in data['kind_cn']:
        items=data['payload']['widgets']
        for item in items:
            bang=item['payload']['subtitle']+item['payload']['title']   #所属榜单
            print(bang)
            datalists=item['subjects']
            for data in datalists:
                movie_id = data['id']  # 电影Id
                movie_name = data['title']  # 电影名
                host_movies_id_and_title[movie_id] = movie_name + " " + bang


    # if 'subjects' in data.keys():
    #     bang=data['payload']['title']    #榜单名称
    #     print(bang)
    #     items=data['subjects']
    #     for item in items:
    #
    #         movie_id=item['id'] #电影Id
    #         movie_name=item['title']    #电影名
    #         # director=item['info'].split('/')[0] #导演
    #         # starring=item['info'].split('/')[1:]    #主演
    #         # country=item['description']     #国别
    #         # rating_num=item['rating']       #评分
    #         # playable=item['playable']       #是否上映
    #         # vote_num=item['rating_count']            #评分人数
    #         host_movies_id_and_title[movie_id]=movie_name+" "+bang
    #     print("=================================================================")
sum=1
for mid, mtitle in host_movies_id_and_title.items():
    print( ' ----->> 正在爬取第 ' + str(sum) + '部影片( ' + mtitle + ' )')
    sum += 1



