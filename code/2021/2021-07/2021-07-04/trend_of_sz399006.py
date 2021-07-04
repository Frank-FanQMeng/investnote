# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import os.path
import pandas as pd
import matplotlib as mpl
import mplfinance as mpf
from cycler import cycler
import akshare as ak

# data
s_code = 'sz399006'
pkl_name = '{}.pkl'.format(s_code)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_zh_index_daily(s_code)
    df.to_pickle(pkl_name)

print(df)

# plot
kwargs = dict(
    type='line',
    mav=(90,),  # 90日均线
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
    marketcolors=mc)

# https://matplotlib.org/stable/gallery/color/named_colors.html
mpl.rcParams['axes.prop_cycle'] = cycler(
    color=['dodgerblue', 'deeppink', 'navy', 'teal', 'maroon', 'darkorange', 'indigo'])
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['axes.unicode_minus'] = False

mpf.plot(df,
         **kwargs,
         style=s,
         datetime_format='%Y-%m-%d',
         show_nontrading=False,
         savefig=dict(fname='{}.jpg'.format(os.path.splitext(os.path.basename(__file__))[0]), bbox_inches='tight'))
