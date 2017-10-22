#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  23 23:29:53 2017

@author: toshiki

１. 「Sphere」などの出力した関数のフォルダをこのプログラムの場所へコピーする。
2. プログラムを実行すると散布図のアニメーションが表示される。
"""
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from plot import outputCompFit


def _update_plot(i, fig, scat_x, scat_pbest, scat_G, swrm_size):
    '''
    print('swrm_size')
    print(swrm_size)
    '''
    min_num = i * swrm_size
    max_num = min_num + swrm_size

    x_sets = np.vstack((horizon_x[min_num:max_num],
                        vertical_x[min_num:max_num])).T
    pbest_sets = np.vstack((horizon_pbest[min_num:max_num],
                            vertical_pbest[min_num:max_num])).T

    '''
    print('x_sets')
    print(x_sets)
    print('pbest_sets')
    print(pbest_sets)
    '''

    scat_x.set_offsets(x_sets)
    scat_pbest.set_offsets(pbest_sets)
    scat_G.set_offsets((horizon_G[i], vertical_G[i]))

    '''
    print(min_num)
    print(max_num)

    print('G')
    print(horizon_G[i])
    print(vertical_G[i])

    print('pbest')
    print(horizon_pbest[min_num:max_num])
    print(vertical_pbest[min_num:max_num])

    print('Frames: %d' % i)
    '''
    plt.title('Generation=' + str(i) + ", Fuction Evaluatio=" + str(min_num))

    return scat_x,


def inputNum(isStr):
    while True:
        num = input('>>>  ')
        if num.isdigit():
            if isStr:
                return num
            else:
                num_int = int(num)
                return num_int
        else:
            print('数値を入力してください')


def getX():
    horizon_x = scatter['X' + x_dim]
    vertical_x = scatter['X' + y_dim]

    return horizon_x, vertical_x


def getPbest():
    horizon_pbest = scatter['pBest' + x_dim]
    vertical_pbest = scatter['pBest' + y_dim]

    return horizon_pbest, vertical_pbest


def getG():
    horizon_G = scatter[scatter['G_index'] == scatter['individual_index']]
    horizon_G = horizon_G['pBest' + x_dim]
    horizon_G.reset_index(drop=True, inplace=True)
    # horizon_G = horizon_G.copy()
    vertical_G = scatter[scatter['G_index'] == scatter['individual_index']]
    vertical_G = vertical_G['pBest' + y_dim]
    vertical_G.reset_index(drop=True, inplace=True)

    return horizon_G, vertical_G

if __name__ == '__main__':
    csv_files = glob.glob('*/RUN*/scatter.csv')
    print('散布図のアニメーションを表示する試行を入力してください。　(Exam: 4)')
    num = inputNum(isStr=False)

    if 0 <= num < len(csv_files):
        outputCompFit(str(num)).plot(x='eval_times', logy=True)
        print('試行' + str(num) + 'の散布図のアニメーションを表示します')
        scatter = pd.read_csv(csv_files[num], header=0, sep=',')

        print("x軸,y軸の次元を選択してください")
        print("x軸の次元 (Exam : 4)")
        x_dim = inputNum(isStr=True)
        print("y軸の次元 (Exam : 4)")
        y_dim = inputNum(isStr=True)

        fig = plt.figure()

        ax = fig.add_subplot(111)
        ax.grid(True, linestyle='-', color='0.75')
        ax.set_xlabel('Dim' + x_dim)
        ax.set_ylabel('Dim' + y_dim)

        horizon_x, vertical_x = getX()
        scat_x = plt.scatter(horizon_x, vertical_x,
                             c='red', marker='.', s=20)
        horizon_pbest, vertical_pbest = getPbest()
        scat_pbest = plt.scatter(horizon_pbest, vertical_pbest,
                                 c='blue', marker='x', s=20)
        horizon_G, vertical_G = getG()
        scat_G = plt.scatter(horizon_G, vertical_G,
                             c='green', marker='*', s=30)

        max_gen = max(scatter['Generation'])
        swrm_size = max(scatter['individual_index']) + 1
        print(swrm_size)
        anim = animation.FuncAnimation(fig, _update_plot,
                                       fargs=(fig, scat_x, scat_pbest, scat_G, swrm_size),
                                       frames=max_gen, interval=1)

        plt.show()

    else:
        print('存在しない試行です')
