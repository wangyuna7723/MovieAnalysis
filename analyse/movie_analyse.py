#!/usr/bin/python
# coding=utf-8

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import jieba
import jieba.analyse
import os
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import TreeMap
from pyecharts.charts import Line
from pyecharts.charts import Boxplot
from pyecharts.charts import Scatter
from pyecharts.faker import Faker
from pyecharts.render import make_snapshot
# 使用 snapshot-selenium 渲染图片
#from snapshot_selenium import snapshot
from snownlp import SnowNLP
import matplotlib as mpl #画图像的库

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class MovieInfoAnalyse(object):
    """
    TOP500电影信息分析类
    """
    csv_path=''
    newRows=''
    def __init__(self):
        self.csv_path = '../movie_info_top500_6.csv'
        # 去空去重
        self.newRows = pd.read_csv(self.csv_path, encoding='utf-8-sig', dtype=str)

        # 去空
        self.newRows.dropna(axis=0,subset=['电影id','名称','类型','国别'],inplace=True)  #只有subset中元素为空才删除
        # 去重
        self.newRows.drop_duplicates(subset=['电影id'],keep='first',inplace=True)
        # # 统计空值
        # print(rows.isnull().sum())
        # print("--------------------------------------")
        # # 统计重复值
        # dup = rows[rows.duplicated()].count()
        # print(dup)

    def make_geo_map(self):
        """
        生成世界地图，根据各国电影发行量
        :return:
        """
        # 对2016-2021数据进行去空去重
        excel_path = '../kettle/2016-2021/file2016-2021.xls'
        rows = pd.read_excel(io=excel_path, sheet_name=0, header=0)
        # 去空
        rows.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        # 移除重复行
        rows.drop_duplicates(subset=['电影id'], keep='first',
                             inplace=True)  # subset参数是一个列表，这个列表是需要你填进行相同数据判断的条件 keep=first时，保留相同数据的第一条。。inplace=True时，会对原数据进行修改。

        # 分析并统计数据
        res = rows['国别'].to_frame()
        # 数据分割
        country_list = []
        for i in res.itertuples():
            for j in i[1].split('/'):
                country_list.append(j)
        # 数据统计
        df = pd.DataFrame(country_list, columns=['国别'])
        res = df.groupby('国别')['国别'].count().sort_values(ascending=False)
        raw_data = [i for i in res.items()]

        # 导入映射数据，英文名 -> 中文名
        country_name = pd.read_json('countries_zh_to_en.json', orient='index')
        stand_data = [i for i in country_name[0].items()]

        # 数据转换
        res_code = {}
        for raw_country in raw_data:
            for stand_country in stand_data:
                if stand_country[1] in raw_country[0]:
                    if (stand_country[0]) in res_code.keys():
                        res_code[stand_country[0]] += raw_country[1]
                    else:
                        res_code[stand_country[0]] = raw_country[1]

        d_order = sorted(res_code.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。# x相当于字典集合中遍历出来的一个元组。
        data = []
        for i in d_order:
            data.append([i[0],i[1]])
        print("==========发行量前10的国家===========")
        for i in range(10):
            print(d_order[i])
        # 制作图表
        c = Map()
        c.add("电影发行量", data, "world")  # 世界地图
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 显示标签
        c.set_global_opts(title_opts=opts.TitleOpts(title="2016-2021年电影TOP500-世界各国电影发行量"),
                          visualmap_opts=opts.VisualMapOpts(
                              max_=600))  # VisualMapOpts：视觉映射配置项，用于显示图例，max_  # 指定 visualMapPiecewise 组件的最大值。
        # 生成html
        #c.render("世界各国电影发行量.html")
        return c


    #2016-2021年中美两国产量对比
    def make_line_AmericanAndChina(self):
        #对2016-2021数据进行去空去重
        excel_path='../kettle/2016-2021/file2016-2021.xls'
        rows=pd.read_excel(io=excel_path,sheet_name=0,header=0)
        # 去空
        rows.dropna(axis=0,how='any',inplace=True)  #axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        # 移除重复行
        rows.drop_duplicates(subset=['电影id'],keep='first',inplace=True) #subset参数是一个列表，这个列表是需要你填进行相同数据判断的条件 keep=first时，保留相同数据的第一条。。inplace=True时，会对原数据进行修改。
        # #统计空值
        # print(rows.isnull().sum())
        # print("--------------------------------------")
        # # 统计重复值
        # dup = rows[rows.duplicated()].count()
        # print(dup)

        to_drop = ['电影id', '名称', '导演', '演员', '语言','类型', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数']
        res = rows.drop(to_drop, axis=1)
        # 数据统计
        American_dict = {}
        China_dict={}
        for i in res.itertuples():  #将DataFrame迭代为元祖。
            if '美国' in i[2]:
                if str(i[1]) in American_dict.keys():
                    American_dict[str(i[1])] += 1
                else:
                    American_dict[str(i[1])]=1
            if '中国大陆' in i[2] or '中国香港' in i[2] or '中国台湾' in i[2] or '中国澳门' in i[2]:
                if str(i[1]) in China_dict.keys():
                    China_dict[str(i[1])] += 1  #发行量+1
                else:
                    China_dict[str(i[1])]=1 #新建

        print("=======美国==========")
        print(American_dict)
        print("=======中国===========")
        print(China_dict)

        American_list=[]
        for k,v in American_dict.items():
            American_list.append(v)
        China_list=[]
        for k,v in China_dict.items():
            China_list.append(v)

        years=['2016','2017','2018','2019','2020','2021']
        # 制作图表
        c = Line()
        c.add_xaxis(years)
        c.add_yaxis("美国发行电影数量", American_list)
        c.add_yaxis("中国发行电影数量", China_list, color=Faker.rand_color())
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="2016-2021年中美电影发行量"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
        # 生成html
        #c.render("2016-2021中美电影发行量.html")

        return c
    #历史电影TOP500榜单中 - 各年份电影发行量
    def make_relase_year_bar(self):
        """
        生成各年份电影发行量柱状图
        :return:
        """

        to_drop = ['排名', '电影id', '名称', '导演', '演员', '国别', '类型', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分析
        res_by = res.groupby('年份')['年份'].count().sort_values(ascending=False)
        res_by2 = res_by.sort_index(ascending=False)
        type(res_by2)
        years = []
        datas = []
        for k, v in res_by2.items():
            years.append(k)
            datas.append(v)
        # 生成图表
        c = Bar()
        c.add_xaxis(years)
        c.add_yaxis("发行电影数量", datas, color=Faker.rand_color())
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="历史电影TOP500榜单中 - 各年份电影发行量"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
        # 生成html
        #c.render("各年份电影发行量.html")

        return c


    #2016-2021中美评分对比
    def make_Boxplot_AmericanAndChina(self):
        # 对2016-2021数据进行去空去重
        excel_path = '../kettle/2016-2021/file2016-2021.xls'
        rows = pd.read_excel(io=excel_path, sheet_name=0, header=0)
        # 去空
        rows.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        # 移除重复行
        rows.drop_duplicates(subset=['电影id'], keep='first',
                             inplace=True)  # subset参数是一个列表，这个列表是需要你填进行相同数据判断的条件 keep=first时，保留相同数据的第一条。。inplace=True时，会对原数据进行修改。
        # #统计空值
        # print(rows.isnull().sum())
        # print("--------------------------------------")
        # # 统计重复值
        # dup = rows[rows.duplicated()].count()
        # print(dup)

        to_drop = ['电影id', '名称','导演', '演员', '语言', '类型', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数']
        res = rows.drop(to_drop, axis=1)
        #统计
        American_dict = {}
        China_dict = {}
        for i in res.itertuples():  # 将DataFrame迭代为元祖。
            if '美国' in i[2]:
                if str(i[1]) not in American_dict.keys():
                    American_score_list = []
                    American_score_list.append(i[3])  # 加入评分
                    American_dict[str(i[1])]=American_score_list
                else:
                    American_score_list.append(i[3])  # 加入评分
            if '中国大陆' in i[2] or '中国香港' in i[2] or '中国台湾' in i[2] or '中国澳门' in i[2]:
                if str(i[1]) not in China_dict.keys():
                    China_score_list = []
                    China_score_list.append(i[3])  # 加入评分
                    China_dict[str(i[1])] = China_score_list
                else:
                    China_score_list.append(i[3])  # 加入评分

        print("==========美国评分============")
        print(American_dict)
        print("==========中国评分============")
        print(China_dict)

        American_list=[]
        for k,v in American_dict.items():
            American_list.append(v)

        China_list = []
        for k, v in China_dict.items():
            China_list.append(v)


        #制作图表
        years = ['2016', '2017', '2018', '2019', '2020', '2021']
        c=Boxplot()
        c.add_xaxis(years)
        c.add_yaxis("美国评分",c.prepare_data(American_list))
        c.add_yaxis("中国评分",c.prepare_data(China_list))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="2016-2021年中美电影评分"),

        )
        #生成html
        #c.render("2016-2021中美电影评分.html")
        return c

    #历史top500电影类型气泡图
    def make_scatter(self):
        to_drop = ['排名', '电影id', '名称', '导演', '演员', '国别', '年份', '语言',  '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        type_dict={}
        for i in res.itertuples():
            for j in i[1].split('/'):
                if j not in type_dict.keys():
                    data=[]
                    data.append([i[2], i[3], i[4]]) #评分 评分人数 短评数
                    type_dict[j]=data   #创建
                else:
                    data=type_dict[j]   #读取之前保存好的信息
                    data.append([i[2], i[3], i[4]]) #新增
                    type_dict[j] =data

        types=[]        #电影类型
        len_types=[]    #每种类型对应的电影数量
        result = {}     #每种类型对应的平均评分 平均评分人数 平均短评数  电影数量
        for k,v in type_dict.items():
            types.append(k)
            len_types.append(len(v))

        # 统计每种类型对应的平均评分 平均评分人数 平均短评数
        for k,v in type_dict.items():
            sum_score = 0
            sum_scorepeople = 0
            sum_commentpeople = 0
            for item in v:
                sum_score+=eval(item[0])
                sum_scorepeople +=eval(item[1])
                sum_commentpeople+=eval(item[2])

            avg_score=(float)(sum_score/len(v))
            avg_scorepeople = (float)(sum_scorepeople / len(v))
            avg_commentpeople = (float)(sum_commentpeople / len(v))

            #print(k+"的平均评分"+str(avg_score)+" 平均评分人数:"+str(avg_scorepeople)+" 平均短评数:"+str(avg_commentpeople))

            result[k]=[avg_score,avg_scorepeople,avg_commentpeople,len(v)]
        print("=================每种类型对应的平均评分 平均评分人数 平均短评数  电影数量=====================")
        print(result)
        #x轴为平均评分，y轴为平均评论人数,s散点大小为对应的电影数量
        x =[]
        y=[]
        s=[]
        for item in result.values():
            x.append(item[0])   #平均评分
            y.append(item[1])    #平均评论人数
            s.append(item[3]*50)    #影片总数

        plt.figure(figsize=(16,10),
                   dpi=120,
                   facecolor='w',
                   edgecolor='k')  # 定义画布，分辨率，背景，边框
        plt.gca().set(xlim=(8.2, 9), ylim=(300000, 1000000))  # 控制横纵坐标的范围
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylabel('平均评论人数', fontsize=22)
        plt.xlabel('平均评分', fontsize=22)
        plt.title("各电影类型平均评分(x轴)-平均评论人数(y轴)-电影数量(气泡大小)", fontsize=22)


        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        for i in range(len(types)):
            """
            未设置“颜色参数c”，调用多次 plt.scatter() 方法生成的多个点是多种不同颜色。 
            """
            plt.scatter(x[i],
                        y[i],
                        s=s[i],
                        alpha=0.7,  # 修改透明度
                        label=types[i],
                        marker="o")

        n = types
        x = x
        y = y
        for a, b, c in zip(x, y, n):
            plt.text(x=a, y=b, s=c, ha='center', va='center', fontsize=10, color='black')
        plt.legend(fontsize=12,markerscale=0.5)#现有图例的0.5倍
        plt.savefig("各电影类型平均评分(x轴)-平均评论人数(y轴)-电影数量(气泡大小).png", dpi=300)

        plt.show()

    #根据电影类型生成饼图
    def make_pie_charts(self):
        """
        根据电影类型生成饼图
        :return:
        """
        to_drop = ['排名','电影id','名称', '导演', '演员', '国别', '年份', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比', '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        type_list = []
        for i in res.itertuples():
            for j in i[1].split('/'):
                type_list.append(j)
        # 数据统计
        df = pd.DataFrame(type_list, columns=['类型'])
        res = df.groupby('类型')['类型'].count().sort_values(ascending=False)
        res_list = []
        for i in res.items():
            res_list.append(i)
        # 生成饼图
        c = Pie()
        c.add("", res_list, center=["40%", "55%"], )
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="历史电影TOP500榜单中 - 各类型占比"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
        # 生成html
        #c.render("各类型占比.html")
        return c

    #生成类型的条形图
    def make_Bar_Types(self):
        to_drop = ['排名', '电影id', '名称', '导演', '演员', '国别', '年份', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        type_list = []
        for i in res.itertuples():
            for j in i[1].split('/'):
                type_list.append(j)
        # 数据统计
        df = pd.DataFrame(type_list, columns=['类型'])
        res = df.groupby('类型')['类型'].count().sort_values(ascending=False)
        res_list = []
        for i in res.items():
            res_list.append(i)

        #x轴为类型，y轴为数量(下面会反转过来，即y轴为类型，x轴为数量)
        types=[]
        sum=[]
        for i in res_list:
            types.append(i[0])
            sum.append(i[1])

        #生成图表
        c = Bar()

        c.add_xaxis(types)
        c.add_yaxis("电影类型", sum, color=Faker.rand_color())
        c.reversal_axis()
        c.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="历史电影TOP500榜单中 - 电影类型"),
            # datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
        # 生成html
        #c.render("电影类型.html")

        return c



    def make_director_treemap(self):
        """
        根据导演电影数生成矩形树图
        :return:
        """

        to_drop = ['排名','电影id','名称', '演员', '年份', '国别', '类型', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比', '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        all_director_list = []
        for i in res.itertuples():
            #     print(i[1] + '\n')
            for j in i[1].split('/'):
                all_director_list.append(j)
        # 数据统计
        df = pd.DataFrame(all_director_list, columns=['导演'])
        res = df.groupby('导演')['导演'].count().sort_values(ascending=False)

        all_director_list = []
        for i in res.items():
            # if i[1] > 4:
                all_director_list.append({"value": i[1], "name": i[0]})
        # 生成图标
        c = TreeMap()
        c.add("导演电影数", all_director_list)
        c.set_global_opts(title_opts=opts.TitleOpts(title="电影TOP500榜单中 - 导演电影数"))
        # 生成html
        c.render("导演电影数.html")

        return c

    # 历史top500中导演人数与影片关系
    def director_work(self):
        """
             根据导演电影数生成矩形图
             :return:
             """

        to_drop = ['排名', '电影id', '名称', '演员', '年份', '国别', '类型', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        all_director_list = []
        for i in res.itertuples():
            #     print(i[1] + '\n')
            for j in i[1].split('/'):
                all_director_list.append(j)
        # 数据统计
        df = pd.DataFrame(all_director_list, columns=['导演'])
        res = df.groupby('导演')['导演'].count().sort_values(ascending=False)

        x=['[0,2)','[2,5)','[5,10)','[10,20)']
        y=[]
        x1=0
        x2=0
        x3=0
        x4=0

        for i in res.items():
            if i[1] in range(0,2):
                x1+=1
            if i[1] in range(2,5):
                x2+=1
            if i[1] in range(5, 10):
                x3 += 1
            if i[1] in range(10, 20):
                x4 += 1

        y.append(x1)
        y.append(x2)
        y.append(x3)
        y.append(x4)
        # 生成图表
        c = Bar()
        c.add_xaxis(x)
        c.add_yaxis("导演人数", y, color=Faker.rand_color())
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="历史top500电影中导演人数-作品数"),
            yaxis_opts=opts.AxisOpts(name="导演人数"),
            xaxis_opts=opts.AxisOpts(name="作品数"),

        )
        # 生成html
        #c.render("历史top500电影中导演人数-作品数.html")
        return c

    def make_star_treemap(self):
        """
        根据演员电影数生成矩形树图
        :return:
        """

        to_drop = ['排名','电影id','名称', '导演', '年份', '国别', '类型', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比', '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        all_star_list = []
        for i in res.itertuples():
            #     print(i[1] + '\n')
            for j in i[1].split('/'):
                all_star_list.append(j)
        # 数据统计
        df = pd.DataFrame(all_star_list, columns=['演员'])
        res = df.groupby('演员')['演员'].count().sort_values(ascending=False)
        all_star_list = []
        for i in res.items():
            if i[1] > 4:
                all_star_list.append({"value": i[1], "name": i[0]})
        # 生成图标
        c = TreeMap()
        c.add("演员电影数", all_star_list)
        c.set_global_opts(title_opts=opts.TitleOpts(title="电影TOP500榜单中 - 演员电影数", subtitle="至少参演5部影评以上"))
        # 生成html
        c.render("演员电影数.html")
        return c

    # 历史top500中演员人数与影片关系
    def star_work(self):
        """
             根据演员电影数生成柱状图
             :return:
             """

        to_drop = ['排名', '电影id', '名称', '导演', '年份', '国别', '类型', '语言', '评分', '评分人数', '五星占比', '四星占比', '三星占比', '二星占比',
                   '一星占比', '短评数',
                   '简介']
        res = self.newRows.drop(to_drop, axis=1)
        # 数据分割
        all_director_list = []
        for i in res.itertuples():
            #     print(i[1] + '\n')
            for j in i[1].split('/'):
                all_director_list.append(j)
        # 数据统计
        df = pd.DataFrame(all_director_list, columns=['演员'])
        res = df.groupby('演员')['演员'].count().sort_values(ascending=False)

        x=['[0,2)','[2,5)','[5,10)','[10,20)']
        y=[]
        x1=0
        x2=0
        x3=0
        x4=0

        for i in res.items():
            if i[1] in range(0,2):
                x1+=1
            if i[1] in range(2,5):
                x2+=1
            if i[1] in range(5, 10):
                x3 += 1
            if i[1] in range(10, 20):
                x4 += 1

        y.append(x1)
        y.append(x2)
        y.append(x3)
        y.append(x4)
        # 生成图表
        c = Bar()
        c.add_xaxis(x)
        c.add_yaxis("演员人数", y, color=Faker.rand_color())
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="历史top500电影演员人数-作品数"),
            yaxis_opts=opts.AxisOpts(name="演员人数"),
            xaxis_opts=opts.AxisOpts(name="作品数"),

        )
        # 生成html
        #c.render("历史top500电影演员人数-作品数.html")
        return c

    """
    按评分进行排序，取前10
	按评论人数进行排序取前10
	按短评数排序取前10
    """
    def sort_Top10(self):
        excel_path= '../kettle/common.xls'
        rows = pd.read_excel(io=excel_path, sheet_name=0, header=0)
        # 去空
        rows.dropna(axis=0, how='any', inplace=True)  # axis=0表示index行  "any"表示这一行或列中只要有元素缺失，就删除这一行或列
        # 移除重复行
        rows.drop_duplicates(subset=['电影id'], keep='first',inplace=True)  # subset参数是一个列表，这个列表是需要你填进行相同数据判断的条件 keep=first时，保留相同数据的第一条。。inplace=True时，会对原数据进行修改。

        # 按评分进行排序，取前10
        b=rows.sort_values(by="评分" , ascending=False) #by 指定列 ascending
        top10_score=b.head(10)
        #print(top10_score)

        # #按评分人数进行排序，取前10
        b = rows.sort_values(by="评分人数", ascending=False)  # by 指定列 ascending
        top10_scorepeople = b.head(10)
        #print(top10_scorepeople)

        # #按短评数进行排序，取前10
        b = rows.sort_values(by="短评数", ascending=False)  # by 指定列 ascending
        top10_commentpeople = b.head(10)
        #print(top10_commentpeople)

        #取交集
        temp=pd.merge(top10_score, top10_scorepeople, how='inner')
        result=pd.merge(top10_commentpeople, temp, how='inner')
        df = result[['电影id', '名称']]
        print(df)


    #情感分析
    def make_sentiments_Pie(self):
        name_list=['疯狂动物城 Zootopia','摔跤吧！爸爸 Dangal','看不见的客人 Contratiempo','釜山行 부산행','血战钢锯岭 Hacksaw Ridge','海边的曼彻斯特 Manchester by the Sea']


        result_list = []
        for movie_name in name_list:
            filename = movie_name + '.csv'
            filpeath='../scrapy/comment/'+filename
            #csv_path='F:\python\豆瓣电影Top500\scrapy\comment\疯狂动物城 Zootopia.csv'
            df = pd.read_csv(filpeath)
            to_drop = ['用户', '是否看过', '评分', '评论时间', '有用数']
            df.drop(to_drop, axis=1, inplace=True)
            str = df.to_string(index=False, columns=['评论'], header=False)
            str = [i.strip() for i in str.split('\n')]

            result = {'positive': 0, 'negative': 0, 'neutral': 0}
            for i in str:
                s = SnowNLP(i)
                if (s.sentiments > 0.66):
                    result['positive'] += 1
                elif (s.sentiments < 0.33):
                    result['negative'] += 1
                else:
                    result['neutral'] += 1
            result_list.append(result)
            # x=[]
            # for v in result.items():
            #     x.append(v)
            #
            # c.add("", x, center=["20%", "30%"], radius=[60, 80], )
        x_lists=[]
        for item in result_list:
            x=[]
            for v in item.items():
                x.append(v)
            x_lists.append(x)
        print("综合排名前6的电影情感得分")
        print(x_lists)

        # 生成图表
        c = Pie()

        c.set_global_opts(
            title_opts=opts.TitleOpts(title="排名前6电影评论的情感分析"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        c.add('', x_lists[0], center=["20%", "30%"], radius=[30, 50], )
        c.add('', x_lists[1], center=["55%", "30%"], radius=[30, 50], )
        c.add('', x_lists[2], center=["20%", "60%"], radius=[30, 50], )
        c.add('', x_lists[3], center=["55%", "60%"], radius=[30, 50], )
        c.add('', x_lists[4], center=["20%", "90%"], radius=[30, 50], )
        c.add('', x_lists[5], center=["55%", "90%"], radius=[30, 50], )

        c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
        # 生成html
        c.render("排名前6电影评论的情感分析.html")

        return c

if __name__ == '__main__':

    m = MovieInfoAnalyse()
    #根据各国电影发行量,生成世界地图
    m.make_geo_map()

    #2016-2021年中美两国电影发行量对比
    m.make_line_AmericanAndChina()

    #历史电影TOP500榜单中 - 各年份电影发行量
    m.make_relase_year_bar()

    ##2016-2021中美评分对比
    m.make_Boxplot_AmericanAndChina()

    #根据电影类型生成饼图
    m.make_pie_charts()

    # 生成类型的条形图
    m.make_Bar_Types()

    # 历史top500电影类型气泡图
    m.make_scatter()

    #导演人数-作品数
    m.director_work()

    #演员人数-作品数
    m.star_work()


    #m.make_star_treemap()
    # m.make_director_treemap()

    #取前10
    m.sort_Top10()

    #情感分析
    m.make_sentiments_Pie()
