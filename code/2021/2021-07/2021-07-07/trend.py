# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)
import pickle

import akshare as ak
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from cycler import cycler


def save_obj(obj, name):
    with open('{}.pkl'.format(name), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


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

zh_names = ('格力电器 美的集团 恒瑞医药 顺丰控股 中国平安 海天味业 兴业银行 海螺水泥 '
            '贵州茅台 五粮液 立讯精密 长春高新 招商银行 长江电力 迈瑞医疗 牧原股份 '
            '上汽集团 中国建筑 伊利股份 隆基股份 三一重工 东方财富 爱尔眼科 中国国旅').split(' ')
s_codes = ['sz000651', 'sz000333', 'sh600276', 'sz002352', 'sh601318', 'sh603288', 'sh601166', 'sh600585',
           'sh600519', 'sz000858', 'sz002475', 'sz000661', 'sh600036', 'sh600900', 'sz300760', 'sz002714',
           'sh600104', 'sh601668', 'sh600887', 'sh601012', 'sh600031', 'sz300059', 'sz300015', 'sh601888']
m_retreat = []
for zh_name, data_name in zip(zh_names, s_codes):
    pkl_name = '{}.pkl'.format(data_name)
    try:
        df = pd.read_pickle(pkl_name)
    except FileNotFoundError:
        df = ak.stock_zh_a_daily(data_name, start_date='20180701')
        df.to_pickle(pkl_name)

    df.set_index('date', inplace=True)
    highest = df.loc[df['close'].idxmax()]['close']
    print(type(highest))
    current = df.iloc[-1]['close']
    print(type(current))
    retreat = -100 * (current - highest) / highest
    m_retreat.append(retreat)
    print(f'{zh_name=} {highest=}, {current=}, {retreat=}%')

    fig, ax = mpf.plot(df,
                       **kwargs,
                       returnfig=True,
                       style=s,
                       datetime_format='%Y-%m-%d',
                       show_nontrading=False)

    fig.text(0.5, 0.5, '老涂数据投研(py_invest_note)',
             fontsize=28, color='gray', alpha=0.5,
             ha='center', va='center', rotation='30')
    fig.legend(['{} 近3年走势'.format(zh_name)], loc='upper center', bbox_to_anchor=(0.5, 0.85))
    plt.savefig(
        fname='{}.jpg'.format(zh_name), bbox_inches='tight')

d = dict(zip(zh_names, m_retreat))
d = {k: v for k, v in sorted(d.items(), key=lambda x: x[1], reverse=True)}
print(d)
save_obj(d, 'retreat')
