# MovieAnalysis
scrapy爬取豆瓣电影top500+分析

scrapy文件夹中包含scrapy爬虫代码。**doubanMovie**为豆瓣电影历史top500，**movie2016-2021**为爬取豆瓣电影2016-2021年top500，**comment**为爬取电影评论

爬虫得到的文件经过kettle抽取，用于**大数据分析的文件**为豆瓣电影历史top500 **movie_info_top500_6.csv**，豆瓣电影2016-2021年top500 **file2016-2021.xls**,6部电影评论存放在**scrapy/comment**

数据分析代码存放在analyse文件夹下，**merge.py**文件为生成可视化大屏-临时，通过拖拽组件后，使用**生成最终大屏.py**，最终生成可视化大屏，可视化大屏如下

![image](https://github.com/wangyuna7723/MovieAnalysis/blob/master/img/%E5%9B%BE43%20%E5%8F%AF%E8%A7%86%E5%8C%96%E5%A4%A7%E5%B1%8F(a).png)
![image](https://github.com/wangyuna7723/MovieAnalysis/blob/master/img/%E5%9B%BE43%20%E5%8F%AF%E8%A7%86%E5%8C%96%E5%A4%A7%E5%B1%8F(b).png)
![image](https://github.com/wangyuna7723/MovieAnalysis/blob/master/img/%E5%9B%BE43%20%E5%8F%AF%E8%A7%86%E5%8C%96%E5%A4%A7%E5%B1%8F(c).png)
![image](https://github.com/wangyuna7723/MovieAnalysis/blob/master/img/%E5%9B%BE43%20%E5%8F%AF%E8%A7%86%E5%8C%96%E5%A4%A7%E5%B1%8F(d).png)
