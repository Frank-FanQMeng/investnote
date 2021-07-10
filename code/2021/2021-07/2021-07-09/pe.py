# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
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
            ha='center', va='center', rotation='0')
    tab = table(ax, data_frame, loc='center', colWidths=col_width)
    tab.auto_set_font_size(False)
    tab.set_fontsize(14)
    tab.scale(1.6, 1.6)
    plt.savefig(image_name, bbox_inches='tight')


# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)

plt.rcParams['font.size'] = 20

zh_names = '格力电器 爱尔眼科 宁德时代'.split(' ')
s_codes = ['000651', '300015', '300750']

for name, code in zip(zh_names, s_codes):
    data_name = 'stock_a_lg_indicator({})'.format(code)
    pkl_name = '{}.pkl'.format(data_name)
    try:
        df = pd.read_pickle(pkl_name)
    except FileNotFoundError:
        df = ak.stock_a_lg_indicator(stock=code)
        df.to_pickle(pkl_name)

    df['total_mv'] = df['total_mv'] / 1e4
    print(name)
    df = df.iloc[:-1]

    print_table_as_image(df.head(n=4), fig_size=(15, 1), col_width=[0.15] + [0.06]*7 + [0.12],
                         image_name='{}_pe表.jpg'.format(name))

    # print(df.loc[df['trade_date'] == pd.to_datetime('2021-03-31')])
    df.set_index('trade_date', inplace=True)
    print(df)

    plt.clf()
    ax1 = df['total_mv'].plot(figsize=(16, 9), style='r-')
    plt.legend(['总市值(亿元)'], loc='upper left', bbox_to_anchor=(0.1, 1.0))
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df['pe'].plot(ax=ax2, style='b-')
    plt.legend(['PE'], loc='upper left', bbox_to_anchor=(0.5, 1.0))
    plt.title('{}总市值与PE走势'.format(name))
    plt.gcf().text(0.5, 0.5, '老涂数据投研(py_invest_note)',
                   fontsize=28, color='gray', alpha=0.5,
                   ha='center', va='center', rotation='30')
    plt.savefig('{}_pe.jpg'.format(name), bbox_inches='tight')
