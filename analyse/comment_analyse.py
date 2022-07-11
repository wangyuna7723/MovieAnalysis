#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import jieba
import jieba.analyse
import os
import time
import pyecharts.options as opts
from pyecharts.charts import WordCloud as eWordCloud
import logging

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class CommentAnalyse:

    def comment_cut_list(self,filename):
        """
        对一部影片的所有影评分词
        :param filename: 文件路径
        :return: segments -> list -> [{'word': '镜头', 'count': 1}, .....]
        """
        pd.set_option('max_colwidth', 500)  ##最大列字符数
        rows = pd.read_csv(filename, encoding='utf-8', dtype=str)
        to_drop = ['用户', '是否看过', '评分', '评论时间', '有用数']
        rows.drop(to_drop, axis=1, inplace=True)
        segments = []
        for index, row in rows.iterrows():
            content = row[0]
            # 第一个参数：待提取关键词的文本
            # 第二个参数：返回关键词的数量，重要性从高到低排序
            # 第三个参数：是否同时返回每个关键词的权重
            # 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
            # 同样是四个参数，但allowPOS默认为('ns', 'n', 'vn', 'v')
            # 即仅提取地名、名词、动名词、动词
            words = jieba.analyse.textrank(content, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
            for word in words:
                segments.append({'word': word, 'count': 1})
        return segments


    def make_frequencies_df(self,segments):
        """
        传入分词list并返回词频统计后的 pandas.DataFrame对象
        :param segments: list -> [{'word': '镜头', 'count': 1}, .....]
        :return: pandas.DataFrame对象
        """
        # 加载停用词表
        stopwords = [line.strip() for line in open('../cn_stopwords.txt', encoding='UTF-8').readlines()]  # list类型
        # 去掉停用词的分词结果  list类型
        text_split_no = []
        for word in segments:
            a = list(word.values())
            if a[0] not in stopwords:
                text_split_no.append(word)

        dfSg = pd.DataFrame(text_split_no)
        dfWord = dfSg.groupby('word')['count'].sum()    #根据word进行count的求和
        return dfWord

    def make_echarts(self,dfword, title):
        """
        利用pyecharts生成词云
        :param dfword: 词频统计后的 pandas.DataFrame对象
        :param title:
        :return:
        """

        htmlName = title + '.html'
        word_frequence = [(k, v) for k, v in dfword.items()]
        # print(word_frequence)
        wc = eWordCloud()
        wc.add(series_name="word", data_pair=word_frequence, word_size_range=[20, 100])
        wc.set_global_opts(title_opts=opts.TitleOpts(
                    title=title, pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
                    tooltip_opts=opts.TooltipOpts(is_show=True))
        wc.render(htmlName)
        return wc

    def make_wordcloud(self):
        name_list = ['疯狂动物城 Zootopia', '摔跤吧！爸爸 Dangal', '看不见的客人 Contratiempo', '釜山行 부산행', '血战钢锯岭 Hacksaw Ridge',
                     '海边的曼彻斯特 Manchester by the Sea']
        for movie_name in name_list:
            filename = movie_name + '.csv'
            filpeath = '../scrapy/comment/' + filename

        ###### pyecharts 生成词云 ######
            segments = self.comment_cut_list(filpeath)
            self.make_echarts(self.make_frequencies_df(segments), movie_name)



if __name__ == '__main__':
    c=CommentAnalyse()
    c.make_wordcloud()