import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv

from constants import *


enc_csv = read_csv(FILE_ENC).apply(pd.to_numeric, errors='coerce')
dup_csv = read_csv(FILE_DUP).apply(pd.to_numeric, errors='coerce')
wri_csv = read_csv(FILE_WRI).apply(pd.to_numeric, errors='coerce')
tot_csv = read_csv(FILE_TOT).apply(pd.to_numeric, errors='coerce')
wif_csv = read_csv(FILE_WFL).apply(pd.to_numeric, errors='coerce')
wid_csv = read_csv(FILE_WTD).apply(pd.to_numeric, errors='coerce')


fig, axes = plt.subplots(2, 2)

df_1 = enc_csv.join(other=[dup_csv, wri_csv, tot_csv])
df_1 = df_1[~df_1.applymap(np.isnan).any(1)]
axes[0, 0].plot(df_1.index, df_1.iloc[0:, 0:])
axes[0, 0].set_title('Затраченное время на каждый документ')
axes[0, 0].set_xlabel('Документы, шт.')
axes[0, 0].set_ylabel('Время, с.')
axes[0, 0].grid(True)


time_sum = 0
time_sum_arr = []
for ind in tot_csv.index:
    time_sum += tot_csv.iat[ind, 0]
    time_sum_arr.append(time_sum)
time_sum_df = pd.DataFrame(data={'TIME_SUM': time_sum_arr})
axes[0, 1].plot(time_sum_df.index, time_sum_df.iloc[0:, 0:])
axes[0, 1].set_title('Суммарное затраченное время')
axes[0, 1].set_xlabel('Документы, шт.')
axes[0, 1].set_ylabel('Время, с.')
axes[0, 1].grid(True)


df_3 = wid_csv[~wid_csv.applymap(np.isnan).any(1)]
axes[1, 0].plot(df_3.index, df_3.iloc[0:, 0:])
axes[1, 0].set_title('Суммарная длина словаря по документам')
axes[1, 0].set_xlabel('Документы, шт.')
axes[1, 0].set_ylabel('Длина словаря')
axes[1, 0].grid(True)


axes[1, 1].plot(time_sum_df['TIME_SUM'], wid_csv['WORDS_NUM_IN_DICT'])
axes[1, 1].set_title('Суммарная длина словаря по времени')
axes[1, 1].set_xlabel('Время, с.')
axes[1, 1].set_ylabel('Длина словаря')
axes[1, 1].grid(True)

plt.show()
