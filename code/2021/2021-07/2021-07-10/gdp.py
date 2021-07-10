# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt

# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)

plt.rcParams.update({'font.size': 20})

data_name = 'macro_china_gdp'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.macro_china_gdp()
    df.to_pickle(pkl_name)

df['国内生产总值-绝对值'] = pd.to_numeric(df['国内生产总值-绝对值'], errors='coerce') / 10000
df['国内生产总值-同比增长'] = pd.to_numeric(df['国内生产总值-同比增长'], errors='coerce')
df = df.loc[df['季度'].str[5:7] == '12']
df = df.iloc[::-1]
print(df)
df.insert(0, '年', df['季度'].apply(lambda x: x[:4]))
df.set_index('年', inplace=True)
print(df)

ax1 = df['国内生产总值-绝对值'].plot(figsize=(16, 9), style='r*-')
plt.legend(['国内生产总值(万亿元)'], loc='upper left', bbox_to_anchor=(0.1, 1.0))
ax2 = ax1.twinx()
ax2.spines['right'].set_position(('axes', 1.0))
df['国内生产总值-同比增长'].plot(ax=ax2, style='bo-')
plt.legend(['增长率(%)'], loc='upper left', bbox_to_anchor=(0.5, 1.0))
plt.gcf().text(0.5, 0.5, '老涂数据投研(py_invest_note)',
               fontsize=28, color='gray', alpha=0.5,
               ha='center', va='center', rotation='30')
plt.savefig('gdp.jpg', bbox_inches='tight')
