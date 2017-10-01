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

csv_files = glob.glob('*/RUN*/output.csv')
# 平均適応度を計算する
mean = pd.read_csv(csv_files[0], header=0, sep=',')
mean = mean - mean
for f in csv_files:
    mean += pd.read_csv(f, header=0, sep=',')

mean /= len(csv_files)
mean = mean.rename(columns={'Best_fitness': 'Mean Fitness'})
mean.to_csv('mean.csv')
print("output mean.csv")
print(mean)

print('平均適応度と比較する試行を入力してください。　(Exam: 4)')
print('全ての試行と比較する場合 : all')
print('平均適応度だけ出力する場合 : mean')
num = input('>>>  ')
if num.isdigit():
    num_int = int(num)

if num == 'mean':
    print('平均適応度を出力します')
    # 平均適応度のプロット
    fit = mean[['eval_times', 'Mean Fitness']]
    fit.plot(x='eval_times', logy=True)     # logスケールでのfitness出力
elif num == 'all':
    print('全ての試行と比較します。')
    # 平均適応度のデータフレーム作成
    fit = mean[['eval_times', 'Mean Fitness']]
    # それぞれの試行をデータフレームに追加
    for f in csv_files:
        rename = re.search(r'RUN\d+', f)
        rename = rename.group(0)
        one_out = pd.read_csv(f, header=0, sep=',')
        one_out = one_out.rename(columns={'Best_fitness': rename})
        fit = pd.concat([fit, one_out[rename]], axis=1)

    fit.plot(x='eval_times', logy=True)     # logスケールでのfitness出力
elif 0 <= num_int < len(csv_files):
    print('試行' + num + 'と平均適応度の比較を出力します')
    file = glob.glob('*/RUN' + num + '/output.csv')
    one_out = pd.read_csv(file[0], header=0, sep=',')
    com_fit = pd.concat([fit, one_out['Best_fitness']], axis=1)
    com_fit = com_fit.rename(columns={'Best_fitness': 'Run' + num})
    com_fit.plot(x='eval_times', logy=True)     # logスケールでのfitness出力else:
else:
    print('存在しない試行です')
