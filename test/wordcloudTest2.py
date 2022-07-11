#-*- codeing=utf-8 -*-
#@Time:2022/6/12 14:37
#@Author:王钰娜
#@File : wordcloudTest2.py
#@Software:PyCharm

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt  # 绘制图像的模块
import jieba.analyse as anls  # 关键词提取
import pandas as pd
import re
from collections import Counter
import pyecharts.options as opts
from pyecharts.charts import WordCloud as eWordCloud

'''功能描述：
   1、读取文本
   2、分词
   3、加载停用词表
   4、去停用词,词频统计
   5、提取关键词2种方法
   6、画词云展示
'''

# 1、读取文本
#text = open("all.txt", 'r', encoding='utf-8').read()
data=pd.read_csv('../scrapy/comment/疯狂动物城 Zootopia.csv', encoding='utf-8')
text_list=data['评论'].values.tolist()
text= ' '.join(text_list)  # list类型分为str
# 加载停用词表
stopwords = [line.strip() for line in open('../cn_stopwords.txt', encoding='UTF-8').readlines()]  # list类型
# 分词未去停用词
text_split = jieba.cut(text)  # 未去掉停用词的分词结果   list类型

# 去掉停用词的分词结果  list类型
text_split_no = []
for word in text_split:
    if word not in stopwords:
        text_split_no.append(word)
# print(text_split_no)

text_split_no_str = ' '.join(text_split_no)  # list类型分为str

# 基于tf-idf提取关键词
print("基于TF-IDF提取关键词结果：")
keywords = []
segments=[]
pd.set_option('max_colwidth', 500)
# 第一个参数：待提取关键词的文本
# 第二个参数：返回关键词的数量，重要性从高到低排序
# 第三个参数：是否同时返回每个关键词的权重
# 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
# 同样是四个参数，但allowPOS默认为('ns', 'n', 'vn', 'v')
# 即仅提取地名、名词、动名词、动词
for words in anls.textrank(text_split_no_str, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v')):
    for word in words:
        segments.append({'word': word, 'count': 1})

#传入分词list并返回词频统计后的 pandas.DataFrame对象
dfSg = pd.DataFrame(segments)
dfWord = dfSg.groupby('word')['count'].sum()
word_frequence = [(k, v) for k, v in dfWord.items()]
# keywords = ' '.join(keywords)  # 转为str
# print(keywords)
#
# # 画词云
# wordcloud = WordCloud(
#     # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
#     font_path="C:/Windows/Fonts/simfang.ttf",
#     # 设置了背景，宽高
#     background_color="white", width=1000, height=880).generate(keywords)  # keywords为字符串类型
#
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()
title='疯狂动物城 Zootopia'
htmlName = title + '2.html'
word_frequence = [(k, v) for k, v in dfWord.items()]
# print(word_frequence)
wc = eWordCloud()
wc.add(series_name="word", data_pair=word_frequence, word_size_range=[20, 100])
wc.set_global_opts(title_opts=opts.TitleOpts(
    title=title, pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
    tooltip_opts=opts.TooltipOpts(is_show=True))
wc.render(htmlName)

