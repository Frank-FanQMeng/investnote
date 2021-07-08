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

data_name = 'macro_china_ppi'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.macro_china_ppi()
    df.to_pickle(pkl_name)

df.insert(1, '年', df['月份'].apply(lambda x: x[:4]))
df['月份'] = df['月份'].apply(lambda x: x[5:7])
df['当月'] = pd.to_numeric(df['当月'], errors='coerce')
df.drop(['当月同比增长', '累计'], axis=1, inplace=True)

print(df)

df = df[df['年'].isin(['2021', '2020', '2019'])]  # df['月份'].str.startswith('2021')
df.sort_values('月份', ascending=True, inplace=True)

print(df)

ax = df.pivot('月份', '年', '当月').plot.bar(figsize=(9, 3), rot=0)
ax.text(0.5, 0.5, '老涂数据投研(py_invest_note)', transform=ax.transAxes,
        fontsize=28, color='gray', alpha=0.5,
        ha='center', va='center', rotation='30')
plt.title('近3年PPI对比')
plt.savefig('ppi.jpg', bbox_inches='tight')
