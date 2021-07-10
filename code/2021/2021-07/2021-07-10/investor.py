# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt

# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

plt.rcParams.update({'font.size': 20})

data_name = 'stock_em_account'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_em_account()
    df.to_pickle(pkl_name)

df.set_index('数据日期', inplace=True)
df = df.iloc[::-1]
df['期末投资者-总量'] = df['期末投资者-总量'] / 10000
df['新增投资者-环比'] = pd.to_numeric(df['新增投资者-环比'], errors='coerce')
df['新增投资者-同比'] = pd.to_numeric(df['新增投资者-同比'], errors='coerce')
df['沪深总市值'] = pd.to_numeric(df['沪深总市值'], errors='coerce') / 10000
df['沪深户均市值'] = pd.to_numeric(df['沪深户均市值'], errors='coerce')
print(df)

fig, ax = plt.subplots(figsize=(16, 9))
fig.text(0.5, 0.5, '老涂数据投研(py_invest_note)',
         fontsize=28, color='gray', alpha=0.5,
         ha='center', va='center', rotation='30')
plt.xticks(rotation=60)
df['期末投资者-总量'].plot(style='r.-', ax=ax)
plt.legend(['期末投资者-总量(亿人)'], loc='upper left')
plt.savefig('investor.jpg', bbox_inches='tight')

plt.clf()
ax1 = df['沪深总市值'].plot(figsize=(16, 9), style='r.-')
plt.legend(['沪深总市值(万亿元)'], loc='upper left', bbox_to_anchor=(0.1, 1.0))
ax2 = ax1.twinx()
ax2.spines['right'].set_position(('axes', 1.0))
df['沪深户均市值'].plot(ax=ax2, style='bo-')
plt.legend(['沪深户均市值(万元)'], loc='upper left', bbox_to_anchor=(0.5, 1.0))
plt.gcf().text(0.5, 0.5, '老涂数据投研(py_invest_note)',
               fontsize=28, color='gray', alpha=0.5,
               ha='center', va='center', rotation='30')
plt.savefig('market_value.jpg', bbox_inches='tight')
