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
import sys
import time


def _update_plot(i, fig, scat_x, scat_pbest, scat_G):
    swrm_size = 3
    min_num = i * swrm_size
    max_num = min_num + swrm_size
    scat_x.set_offsets((horizon_x[min_num:max_num],
                        vertical_x[min_num:max_num]))
    scat_pbest.set_offsets((horizon_pbest[min_num:max_num],
                            vertical_pbest[min_num:max_num]))
    scat_G.set_offsets((horizon_G[i], vertical_G[i]))

    print(min_num)
    print(max_num)
    
    print('G')
    print(horizon_G[i])
    print(vertical_G[i])
    
    print('pbest')
    print(horizon_pbest[min_num:max_num])
    print(vertical_pbest[min_num:max_num])
    
    print('Frames: %d' % i)
    # if i == 0:
    #    time.sleep(10)
    plt.title('Generation=' + str(i) + ", Fuction Evaluatio=" + str(min_num))

    return scat_x,

csv_files = glob.glob('*/RUN*/scatter.csv')


print('散布図のアニメーションを表示する試行を入力してください。　(Exam: 4)')
num = input('>>>  ')
if num.isdigit():
    num_int = int(num)

if 0 <= num_int < len(csv_files):
    print('試行' + num + 'の散布図のアニメーションを表示します')
    file = glob.glob('*/RUN' + num + '/scatter.csv')
    scatter = pd.read_csv(csv_files[0], header=0, sep=',')

    eval_times = scatter['eval_times']
    eval_times = eval_times.drop_duplicates()

    print("x軸,y軸の次元を選択してください")
    print("x軸の次元 (Exam : 4)")
    x_dim = input('>>>  ')
    print("y軸の次元 (Exam : 4)")
    y_dim = input('>>>  ')

    horizon_x = scatter['X' + x_dim]
    vertical_x = scatter['X' + y_dim]

    horizon_pbest = scatter['pBest' + x_dim]
    vertical_pbest = scatter['pBest' + y_dim]

    horizon_G = scatter[scatter['G_index'] == scatter['individual_index']]
    horizon_G = horizon_G['pBest' + x_dim]
    horizon_G.reset_index(drop=True, inplace=True)
    # horizon_G = horizon_G.copy()
    vertical_G = scatter[scatter['G_index'] == scatter['individual_index']]
    vertical_G = vertical_G['pBest' + y_dim]
    vertical_G.reset_index(drop=True, inplace=True)

    # sys.exit()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.grid(True, linestyle='-', color='0.75')
    ax.set_xlabel('Dim' + x_dim)
    ax.set_ylabel('Dim' + y_dim)

    scat_x = plt.scatter(horizon_x, vertical_x,
                         c='red', marker='.', s=60)
    scat_pbest = plt.scatter(horizon_pbest, vertical_pbest,
                             c='blue', marker='x', s=20)
    scat_G = plt.scatter(horizon_G, vertical_G,
                         c='green', marker='*', s=10)

    max_gen = max(scatter['Generation'])
    anim = animation.FuncAnimation(fig, _update_plot,
                                   fargs=(fig, scat_x, scat_pbest, scat_G),
                                   frames=max_gen, interval=100)

    plt.show()


else:
    print('存在しない試行です')
