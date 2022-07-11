#-*- codeing=utf-8 -*-
#@Time:2022/6/12 20:47
#@Author:王钰娜
#@File : 生成最终大屏.py
#@Software:PyCharm
from pyecharts.charts import Page

# 执行之前,请确保:1、已经把json文件放到本目录下 2、把json中的title和table的id替换掉
Page.save_resize_html(
    source="大屏_临时.html",
    cfg_file="chart_config (1).json",
    dest="大屏_最终.html"
)