import os
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv

from constants import *

curr_dir = FIRST_DIR
enc_path = os.path.join(curr_dir, FILE_ENC)
dup_path = os.path.join(curr_dir, FILE_DUP)
wri_path = os.path.join(curr_dir, FILE_WRI)
tot_path = os.path.join(curr_dir, FILE_TOT)
wif_path = os.path.join(curr_dir, FILE_WFL)
wid_path = os.path.join(curr_dir, FILE_WTD)


enc_csv = read_csv(enc_path).apply(pd.to_numeric, errors='coerce')
dup_csv = read_csv(dup_path).apply(pd.to_numeric, errors='coerce')
wri_csv = read_csv(wri_path).apply(pd.to_numeric, errors='coerce')
tot_csv = read_csv(tot_path).apply(pd.to_numeric, errors='coerce')
wif_csv = read_csv(wif_path).apply(pd.to_numeric, errors='coerce')
wid_csv = read_csv(wid_path).apply(pd.to_numeric, errors='coerce')

enc_csv = enc_csv[~enc_csv.applymap(np.isnan).any(1)]
dup_csv = dup_csv[~dup_csv.applymap(np.isnan).any(1)]
wri_csv = wri_csv[~wri_csv.applymap(np.isnan).any(1)]
tot_csv = tot_csv[~tot_csv.applymap(np.isnan).any(1)]
wif_csv = wif_csv[~wif_csv.applymap(np.isnan).any(1)]
wid_csv = wid_csv[~wid_csv.applymap(np.isnan).any(1)]


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

enc_sum = 0
dup_sum = 0
wri_sum = 0
tot_sum = 0
other_sum = 0

for ind in dup_csv.index:
    tot_sum += tot_csv.iat[ind - 1, 0]
    enc_sum += enc_csv.iat[ind - 1, 0]
    dup_sum += dup_csv.iat[ind - 1, 0]
    wri_sum += wri_csv.iat[ind - 1, 0]
other_sum = tot_sum - enc_sum - dup_sum - wri_sum

print(tot_sum)
print(enc_sum)
print(dup_sum)
print(wri_sum)
print(other_sum)
d = {
        'TOTAL': tot_sum,
        'ENCODING': enc_sum,
        'DUPLICATE': dup_sum,
        'WRITING': wri_sum,
        'OTHER': other_sum,
    }
OrderedDict(sorted(d.items(), key=lambda item: item[1]))
for item in d.items():
    print(item)
fig, ax = plt.subplots()
p = ax.bar(np.arange(1, 6), list(reversed(sorted([tot_sum, enc_sum, dup_sum, wri_sum, other_sum]))))
ax.set_xticks(np.arange(1, 6), list([x[0] for x in d.items()]))
ax.bar_label(p, label_type='center')
plt.show()
