#-*- codeing=utf-8 -*-
#@Time:2022/3/31 0:02
#@Author:王钰娜
#@File : start.py
#@Software:PyCharm

from scrapy import cmdline
import time

t0 = time.time()
print('显示程序开始的时间:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
cmdline.execute("scrapy crawl MovieComment".split())
t1=time.time()
print('显示程序结束的时间:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print("用时：%.6fs"%(t1-t0))