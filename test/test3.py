#-*- codeing=utf-8 -*-
#@Time:2022/6/3 2:54
#@Author:王钰娜
#@File : test3.py
#@Software:PyCharm

# 爬取评论
# 前10的影评
data = {}
for i, (k, v) in enumerate(self.movies_id_and_title_dict.items()):
    data[k] = v
    if i == 9:
        print(data)
        break
number = 1
for movie_id, movie_name in data.items():
    print(get_current_time() + ' ----->> 正在爬取第 ' + str(number) + '部影片( ' + movie_name + ' )评论')
    number += 1
"""
    爬取指定影片的短评并写入csv文件（文件以影片名命名）
    :param movie_id:
    :param movie_name:
    :return:
    """
base_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/comments?start={}&limit=20&status=P&sort=new_score'
all_page_comments = [base_url.format(x) for x in range(0, 201, 20)]

CommentItem = commentItem()  # 实例化电影评论
CommentItem['movie_name'] = movie_name

for each_page_comments in all_page_comments:
    time.sleep(1)
    yield Request(each_page_comments, meta={"item": CommentItem}, headers=header, cookies=cookies,
                  callback=self.get_comments)
