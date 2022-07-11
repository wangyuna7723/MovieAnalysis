#-*- codeing=utf-8 -*-
#@Time:2022/6/8 15:06
#@Author:王钰娜
#@File : ChangeCsvToXls.py
#@Software:PyCharm

# -*- coding: utf-8 -*-
import csv
import os
import xlrd
import xlwt


def csv_2_xls():
        csvfile='movie_info_top500_6.csv'
        filename='move_info_top500'
        xlsfile =filename + '.xls'
        with open(csvfile, 'r',encoding='utf8') as f:
            reader = csv.reader(f)
            workbook = xlwt.Workbook()  #创建工作簿
            sheet = workbook.add_sheet('sheet1')  # 创建一个sheet表格
            i = 0
            for line in reader:
                j = 0
                for v in line:
                    sheet.write(i, j, v)
                    j += 1
                i += 1
            workbook.save(xlsfile)  # 保存Excel
        print(f'转换完成: {csvfile} -> {xlsfile}')



if __name__ == '__main__':
    csv_2_xls()
