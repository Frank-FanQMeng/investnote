# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table


def print_table_as_image(data_frame, fig_size, col_width, image_name):
    """
    将数据打印为图片
    """
    fig, ax = plt.subplots(figsize=fig_size)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    ax.text(0.5, 0.5, '老涂数据投研(py_invest_note)', transform=ax.transAxes,
            fontsize=28, color='gray', alpha=0.5,
            ha='center', va='center', rotation='30')
    tab = table(ax, data_frame, loc='center', colWidths=col_width)
    tab.auto_set_font_size(False)
    tab.set_fontsize(14)
    tab.scale(1.6, 1.6)
    plt.savefig(image_name)


# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)

data_name = 'sw_index_spot'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.sw_index_spot()
    df.to_pickle(pkl_name)

print(df)

total_count = 0
each_count = dict()
year_count = dict()
month_count = dict()
for code, name in zip(df.指数代码, df.指数名称):
    data_name = 'ak.sw_index_cons({})'.format(code)
    pkl_name = '{}.pkl'.format(data_name)
    try:
        df = pd.read_pickle(pkl_name)
    except FileNotFoundError:
        df = ak.df = ak.sw_index_cons(index_code=code)
        df.to_pickle(pkl_name)

    print(name)
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    print(df)
    print(f"{df['weight'].sum()=}")
    print(type(df))
    for ind, row in df.iterrows():
        # print(ind, row, type(row['start_date']))
        year = row['start_date'].strftime('%Y')
        month = row['start_date'].strftime('%Y-%m')
        print(month)
        year_count[year] = year_count.get(year, 0) + 1
        month_count[month] = month_count.get(month, 0) + 1

    df.sort_values('weight', ascending=False, inplace=True)
    print(df)
    df.drop(['start_date'], axis=1, inplace=True)
    df.rename(columns={'stock_code': '代码', 'stock_name': '名称', 'weight': '权重'}, inplace=True)
    print_table_as_image(df.head(n=20), fig_size=(6, 6), col_width=([0.2] * 3),
                         image_name='{}_top20.jpg'.format(name))
    each_count[name] = df.index.size
    total_count += df.index.size

print(each_count)
print(total_count)
year_count = {k: v for k, v in sorted(year_count.items())}
print(year_count)
month_count = {k: v for k, v in sorted(month_count.items())}
print(month_count)

ind = list(range(len(each_count)))
y = list(each_count.values())
plt.clf()
f = plt.figure(figsize=(6, 12))
plt.barh(ind, y, 0.8)
plt.yticks(ticks=ind, labels=list(each_count.keys()))
for i, v in enumerate(y):
    plt.text(v + 3, i, str(v), color='red', fontweight='normal')
f.text(0.5, 0.5, '老涂数据投研(py_invest_note)',
       fontsize=28, color='gray', alpha=0.5,
       ha='center', va='center', rotation='30')
plt.title('申万一级分布')
plt.savefig(
    fname='sw_cons.jpg', bbox_inches='tight')
