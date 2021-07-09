# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import akshare as ak
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from cycler import cycler

# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)

# plot
kwargs = dict(
    type='line',
    mav=(30,),  # 30日均线
    volume=False,  # 不显示成交量
    title='',
    ylabel='',
    ylabel_lower='',
    fontscale=2,
    figratio=(16, 9),  # 宽高比
    figscale=1.6)  # 图片大小

mc = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='i',
    wick='i',
    volume='i',
    inherit=True)

s = mpf.make_mpf_style(
    gridaxis='both',
    gridstyle='-.',
    y_on_right=False,
    marketcolors=mc,
    rc={'font.sans-serif': 'SimHei'})

# https://matplotlib.org/stable/gallery/color/named_colors.html
mpl.rcParams['axes.prop_cycle'] = cycler(
    color=['dodgerblue', 'deeppink', 'navy', 'teal', 'maroon', 'darkorange', 'indigo'])
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['axes.unicode_minus'] = False

data_name = 'sw_index_spot'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.sw_index_spot()
    df.to_pickle(pkl_name)

print(df)

for code, name in zip(df.指数代码, df.指数名称):
    data_name = 'sw_index_daily({})'.format(code)
    pkl_name = '{}.pkl'.format(data_name)
    try:
        df = pd.read_pickle(pkl_name)
    except FileNotFoundError:
        df = ak.sw_index_daily(index_code=code, start_date='2018-07-01', end_date='2021-07-08')
        df.to_pickle(pkl_name)
    df = df.iloc[::-1]
    df.set_index('date', inplace=True)
    df.drop(['index_code', 'index_name'], axis=1, inplace=True)
    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    fig, ax = mpf.plot(df,
                       **kwargs,
                       returnfig=True,
                       style=s,
                       datetime_format='%Y-%m-%d',
                       show_nontrading=False)

    fig.text(0.5, 0.5, '老涂数据投研(py_invest_note)',
             fontsize=28, color='gray', alpha=0.5,
             ha='center', va='center', rotation='30')
    fig.legend(['申万一级分类-{} 近3年走势'.format(name)], loc='upper center', bbox_to_anchor=(0.5, 0.85))
    plt.savefig(
        fname='{}.jpg'.format(name), bbox_inches='tight')
