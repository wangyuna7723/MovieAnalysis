#-*- codeing=utf-8 -*-
#@Time:2022/6/12 16:30
#@Author:王钰娜
#@File : Merge.py
#@Software:PyCharm
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
from pyecharts.charts import Page,Bar
from pyecharts.components import Table

from analyse.movie_analyse import MovieInfoAnalyse
from analyse.comment_analyse import CommentAnalyse



def make_wordcloud(filpeath,title):
		"""
		     对一部影片的所有影评分词
		     :param filename: 文件路径
		     :return: segments -> list -> [{'word': '镜头', 'count': 1}, .....]
		     """
		pd.set_option('max_colwidth', 500)  ##最大列字符数
		rows = pd.read_csv(filpeath, encoding='utf-8', dtype=str)
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
		dfWord = dfSg.groupby('word')['count'].sum()  # 根据word进行count的求和

		htmlName = title + '.html'
		word_frequence = [(k, v) for k, v in dfWord.items()]
		# print(word_frequence)
		wc = eWordCloud()
		wc.add(series_name="word", data_pair=word_frequence, word_size_range=[20, 100])
		wc.set_global_opts(title_opts=opts.TitleOpts(
			title=title, pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
			tooltip_opts=opts.TooltipOpts(is_show=True))
		wc.render(htmlName)
		return wc

def text_line(text):
	table = Table()
	table.add(headers=[text], rows=[])
	#table.render(text+'.html')
	print('生成完毕:'+text+'.html')
	return table

def pic():
	pic=Bar(init_opts=opts.InitOpts(width="800px",height="600px"))
	pic.set_global_opts(

	graphic_opts = [
					   opts.GraphicImage(
						   graphic_item=opts.GraphicItem(
							   id_="logo", right=20, top=8, z=-10, bounding="raw",
						   ),
						   graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
							   image='各电影类型平均评分(x轴)-平均评论人数(y轴)-电影数量(气泡大小).png',
							   width=800,
							   height=600,
							   ),
					   )
				   ],)

	return pic



if __name__ == '__main__':

	name_list = ['疯狂动物城 Zootopia', '摔跤吧！爸爸 Dangal', '看不见的客人 Contratiempo', '釜山行 부산행', '血战钢锯岭 Hacksaw Ridge',
				 '海边的曼彻斯特 Manchester by the Sea']
	result = []
	for movie_name in name_list:
		filename = movie_name + '.csv'
		filpeath = '../scrapy/comment/' + filename
		result.append(make_wordcloud(filpeath,movie_name))  # 生成词云


	m = MovieInfoAnalyse()
	c = CommentAnalyse()
	page = Page(layout=Page.DraggablePageLayout, page_title="豆瓣电影分析")

	# 在页面中添加图表
	page.add(
		m.make_geo_map(),  # 根据各国电影发行量,生成世界地图
		m.make_line_AmericanAndChina(),  # 2016-2021年中美两国电影发行量对比
		m.make_relase_year_bar(),  # 历史电影TOP500榜单中 - 各年份电影发行量
		m.make_Boxplot_AmericanAndChina(),  ##2016-2021中美评分对比
		m.make_pie_charts(),  # 根据电影类型生成饼图
		m.make_Bar_Types(),  # 生成类型的条形图
		m.make_scatter(),							# 历史top500电影类型气泡图
		m.director_work(),  # 历史top500中导演人数与影片关系
		m.star_work(),  # 历史top500中演员人数与影片关系
		m.sort_Top10(),								# 取前10电影




	)
	page.add(
		# 生成几个文本
		text_line("2016-2021年中美对比"),
		text_line("历史top500电影"),
		text_line("综合排名前6电影"),

		#添加气泡图
		pic()

	)
	page.add(

		m.make_sentiments_Pie(),							## 前6电影的情感分析
		#排名前6的电影评论词云
		result[0],
		result[1],
		result[2],
		result[3],
		result[4],
		result[5],

	)
	page.render('大屏_临时.html')  # 执行完毕后,打开临时html并排版,排版完点击Save Config，把json文件放到本目录下
	print('生成完毕:大屏_临时.html')


