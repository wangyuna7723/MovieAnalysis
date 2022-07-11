#-*- codeing=utf-8 -*-
#@Time:2022/6/8 19:38
#@Author:王钰娜
#@File : ChangeCsvToTxt.py
#@Software:PyCharm

# CSV-->TXT文件(将demo里面的'副本_Stu_Exe.csv'文件)

fr = open('movie_info_top500_6.csv', 'r',encoding='utf-8')
fw = open('movie_info_top500.txt', 'w+',encoding='utf-8')

ls = []

for line in fr:
    line = line.replace('\n', '')  # 删除每行后面的换行符
    line = line.split(',')  # 将每行数据以逗号切割成单个字符
    ls.append(line)  # 将单个字符追加到列表ls中

for row in ls:
    fw.write(' '.join(row) + '\n')

fr.close()
fw.close()
