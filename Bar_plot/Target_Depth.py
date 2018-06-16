#!/usr/bin/python3
#coding: utf-8 
#Email: songzhiruifly@hotmail.com
#Date: 2018-10-09 09:14:37
"""
输入文件：bed文件及基于bed文件提取的深度结果文件。
a.bed:
chr19   5851262 5851999
dd.xls:
chr19   5851262 58
"""

from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

def subfig(nrow, ncol, i, x, y, title):
    fig = plt.subplot(nrow, ncol, i) #根据bed区间的个数来确定子图个数，N行1列
    plt.sca(fig) #在指定子图中进行下面的绘制
    plt.bar(x, y) #绘制柱状图
    plt.title("%s: %s - %s"%title) #图标题
    plt.xlim((x[0] - 1, x[-1] + 1)) #x轴范围
    plt.ylim((min(y) - 5, max(y) + 5))
    fmt = "%d"
    xticks = mtick.FormatStrFormatter(fmt) #格式化x轴数字输出，默认为科学计数
    axes = plt.gca()
    axes.xaxis.set_major_formatter(xticks)

info_dict = OrderedDict()
with open("dd.xls") as ii, open("a.bed") as bed:
    Chr = set()
    for b in bed: #根据bed文件来确定子图个数
        Chromose, Start, End = b.strip().split("\t")
        Chr.add(Chromose)
        info_dict[(Chromose, int(Start), int(End))] = ([], [])

    for i in ii: #从深度结果中提取信息
        chromose, start, depth = i.strip().split("\t")
        if chromose in Chr:
            for i in info_dict.keys():
                c, s, e = i
                if chromose == c and s <= int(start) <= int(e):
                    info_dict[i][0].append(int(start))
                    info_dict[i][1].append(int(depth))

m, n , l = len(info_dict.keys()), 1, 1
plt.figure(num=1) #打开画布，编号为一个说明所有的子图绘制到一个图片中
for i, j in info_dict.items():
    x = np.array(j[0])
    y = np.array(j[1])
    subfig(m, n, l, x, y, i)
    l += 1


plt.subplots_adjust(hspace=0.5) #调整子图之间的距离
plt.show() 
#plt.savefig("1.png")
