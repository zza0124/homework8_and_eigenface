import numpy as np
import matplotlib.pylab as plt
from calculated import variance
import math
from calculated import CHAZHI
import os
import re
im=plt.imread('lena512color.tiff')
a=im
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])
im=rgb2gray(im)
sh=np.shape(im)
print(sh)
b=np.ones((sh[0],sh[1]),np.float64)
# tim=float(input('请输入放大系数（输入数是小于1的正数时为放缩）,大于1的倍数将取整：'))
tim=2
def plti(im,**kwargs):
    plt.imshow(im,interpolation='none',**kwargs)
    plt.axis('off')
    plt.savefig('d:/new.jpeg')
    plt.show()
print(sh[0],type(im[1,1]))
if tim <=1:
    timd=int(1/tim)
    b=im[::timd,::timd]
if tim >1:
    sh = np.shape(im)
    b = np.ones((sh[0], sh[1]), np.float64)
    tim = int(tim)
    b = np.ones((sh[0] * tim - tim + 1, sh[1] * tim - tim + 1), np.float64)
    b[::tim, ::tim] = im
    print('正在初始化请等待...')
    if(tim%2==0):
        for i in range(sh[0]):
            for j in range(sh[1] - 1):
                try:
                    a1 = [im[i, j - 2], im[i, j - 1], im[i, j], im[i, j + 1]]
                    s1 = variance.variance(a1)
                except IndexError as e:
                    s1 = 10000
                try:
                    a2 = [im[i, j - 1], im[i, j], im[i, j + 1], im[i, j + 2]]
                    s2 = variance.variance(a2)
                except IndexError as e:
                    s2 = 10000
                try:
                    a3 = [im[i, j], im[i, j + 1], im[i, j + 2], im[i, j + 3]]
                    s3 = variance.variance(a3)
                except IndexError as e:
                    s3 = 10000
                if min(s1, s2, s3) == s1:
                    imp = a1
                    X = [j - 2, j - 1, j, j + 1]
                if min(s1, s2, s3) == s2:
                    imp = a2
                    X = [j - 1, j, j + 1, j + 2]
                if min(s1, s2, s3) == s3:
                    imp = a3
                    X = [j, j + 1, j + 2, j + 3]
                if tim == 2:
                    b[tim * i, tim * j + 1] = CHAZHI.lagrange(np.dot(X, tim), imp, tim * j + 1)
                if tim > 2:
                    for k in range(tim - 1):
                        x0 = np.add(np.dot(np.ones(tim - 1), tim * i), list(range(tim - 1)))
                        b[tim * i:tim * i + tim, j] = CHAZHI.lagrange(tim * X, imp, x0)
        b = b.T
        for i in range((sh[0] * tim) - 1):
            print('加载中：',i,'/',(sh[0] * tim) - 1)
            for j in range(sh[1] - 1):
                try:
                    a1 = [b[i, (j - 2)*tim], b[i, (j - 1)*tim], b[i, j*tim], b[i, (j + 1)*tim]]
                    s1 = variance.variance(a1)
                except IndexError as e:
                    s1 = 10000
                try:
                    a2 = [b[i, j*tim - 1*tim], b[i, j*tim], b[i, j *tim+ 1*tim], b[i, j *tim+ 2*tim]]
                    s2 = variance.variance(a2)
                except IndexError as e:
                    s2 = 10000
                try:
                    a3 = [b[i, j*tim], b[i, j*tim + 1*tim], b[i, j*tim + 2*tim], b[i, j *tim+ 3*tim]]
                    s3 = variance.variance(a3)
                except IndexError as e:
                    s3 = 10000
                if min(s1, s2, s3) == s1:
                    imp = a1
                    X = [j - 2, j - 1, j, j + 1]
                if min(s1, s2, s3) == s2:
                    imp = a2
                    X = [j - 1, j, j + 1, j + 2]
                if min(s1, s2, s3) == s3:
                    imp = a3
                    X = [j, j + 1, j + 2, j + 3]
                if tim == 2:
                    b[i, tim * j + 1] = CHAZHI.lagrange(np.dot(X, tim), imp, tim * j + 1)
                if tim > 2:
                    for k in range(tim - 1):
                        x0 = np.add(np.dot(np.ones(tim - 1), tim * i), list(range(tim - 1)))
                        b[i:tim * i + tim, j] = CHAZHI.lagrange(tim * X, imp, x0)
        b=b.T
        print(b)
        plti(b)
plti(b)
print('目前只是实现了放大二倍的操作，更高倍数因为时间问题有待完善')