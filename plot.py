#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 23:29:53 2017

@author: toshiki

１. 「Sphere」などの出力した関数のフォルダをこのプログラムの場所へコピーする。
2. プログラムを実行すると平均適応度のプロット及び、平均と特定の試行を比較したプロットが出力される。
"""
import pandas as pd
import glob
import re


def getMean():
    csv_files = glob.glob('*/RUN*/output.csv')
    # 平均適応度を計算する
    mean = pd.read_csv(csv_files[0], header=0, sep=',')
    mean = mean - mean
    for f in csv_files:
        mean += pd.read_csv(f, header=0, sep=',')

    mean /= len(csv_files)
    mean = mean.rename(columns={'Best_fitness': 'Mean Fitness'})
    mean.to_csv('mean.csv')
    # print("output mean.csv")
    # print(mean)

    return mean, csv_files


def outputMeanFit():
    print('平均適応度を出力します')
    mean, csv_files = getMean()
    # 平均適応度のプロット
    fit = mean[['eval_times', 'Mean Fitness']]

    return fit


def outputAllFit():
    print('全ての試行と比較します。')
    # 平均適応度のデータフレーム作成
    mean, csv_files = getMean()
    fit = mean[['eval_times', 'Mean Fitness']]
    # それぞれの試行をデータフレームに追加
    for f in csv_files:
        rename = re.search(r'RUN\d+', f)
        rename = rename.group(0)
        one_out = pd.read_csv(f, header=0, sep=',')
        one_out = one_out.rename(columns={'Best_fitness': rename})
        fit = pd.concat([fit, one_out[rename]], axis=1)

    return fit


def outputCompFit(num):
    mean, csv_files = getMean()
    if num.isdigit():
        num_int = int(num)
    else:
        print('数字を入力してください')
        return

    if num_int < 0 or len(csv_files) <= num_int:
        print('存在しない試行です')
        return

    print('試行' + num + 'と平均適応度の比較を出力します')
    fit = mean[['eval_times', 'Mean Fitness']]
    file = glob.glob('*/RUN' + num + '/output.csv')
    one_out = pd.read_csv(file[0], header=0, sep=',')
    com_fit = pd.concat([fit, one_out['Best_fitness']], axis=1)
    com_fit = com_fit.rename(columns={'Best_fitness': 'Run' + num})
    
    return com_fit


if __name__ == '__main__':
    print('平均適応度と比較する試行を入力してください。　(Exam: 4)')
    print('全ての試行と比較する場合 : all')
    print('平均適応度だけ出力する場合 : mean')

    num = input('>>>  ')
    if num.isdigit():
        num_int = int(num)

    if num == 'mean':
        outputMeanFit().plot(x='eval_times', logy=True)
    elif num == 'all':
        outputAllFit().plot(x='eval_times', logy=True)
    elif num.isdigit():
        outputCompFit(num).plot(x='eval_times', logy=True)
    else:
        print('Invalid input')
