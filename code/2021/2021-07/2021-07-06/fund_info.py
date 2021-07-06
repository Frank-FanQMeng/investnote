# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pandas as pd
import akshare as ak
from pandas.plotting import table
import matplotlib.pyplot as plt


def print_table_as_image(data_frame, fig_size, col_width, image_name):
    """
    将数据打印为图片
    """
    fig, ax = plt.subplots(figsize=fig_size)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    ax.text(0.5, 0.5, '老涂数据投研(py_invest_note)', transform=ax.transAxes,
            fontsize=20, color='gray', alpha=0.5,
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

# 基金公司
data_name = 'fund_em_aum'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.fund_em_aum()
    df.to_pickle(pkl_name)

print(df)
print(df.columns)
print(df.index.size)
print(f"{df['全部管理规模'].sum()=}")
print(f"{df['全部基金数'].sum()=}")
print(f"{df['全部经理数'].sum()=}")

fund_top10 = df[['基金公司', '成立时间', '全部管理规模', '全部基金数', '全部经理数']].head(n=10)
print(fund_top10)
print_table_as_image(fund_top10, (8, 4), ([0.3, 0.12, 0.12, 0.12, 0.12]),
                     'fund_top10.jpg')

# 基金基本信息
data_name = 'fund_em_fund_name'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.fund_em_fund_name()
    df.to_pickle(pkl_name)

print(df)
print(df.columns)
print(df.index.size)

# 按照基金类型分类
fund_by_type = df.groupby(['基金类型'], as_index=False).size()
fund_by_type.rename(columns={'size': '数量'}, inplace=True)
print(fund_by_type)
print_table_as_image(fund_by_type, (3, 5), [0.28] * len(fund_by_type.columns), 'fund_by_type.jpg')

# 股票型基金排名
data_name = 'fund_em_open_fund_rank'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.fund_em_open_fund_rank(symbol='股票型')
    df.to_pickle(pkl_name)

print(df)
print(df.columns)
print(df.index.size)
df['今年来'] = pd.to_numeric(df['今年来'], errors='coerce')
df['近1年'] = pd.to_numeric(df['近1年'], errors='coerce')
df['近3年'] = pd.to_numeric(df['近3年'], errors='coerce')

# 今年来收益排名
fund_by_this_year = df.sort_values('今年来', ascending=False)
print(fund_by_this_year)
fund_by_this_year_top10 = fund_by_this_year[['基金代码', '基金简称', '近3年', '近2年', '近1年', '今年来']].head(n=10)
fund_by_this_year_top10.reset_index(drop=True, inplace=True)
print(fund_by_this_year_top10)
print_table_as_image(fund_by_this_year_top10, (10, 4), ([0.08, 0.22] + [0.08] * (len(fund_by_this_year_top10) - 2)),
                     'fund_by_this_year_top10.jpg')

# 近1年收益排名
fund_by_year = df.sort_values('近1年', ascending=False)
print(fund_by_year)
fund_by_year_top10 = fund_by_year[['基金代码', '基金简称', '近3年', '近2年', '近1年', '今年来']].head(n=10)
fund_by_year_top10.reset_index(drop=True, inplace=True)
print(fund_by_year_top10)
print_table_as_image(fund_by_year_top10, (10, 4), ([0.08, 0.22] + [0.08] * (len(fund_by_year_top10) - 2)),
                     'fund_by_year_top10.jpg')

# 近3年收益排名
fund_by_3year = df.sort_values('近3年', ascending=False)
print(fund_by_3year)
fund_by_3year_top10 = fund_by_3year[['基金代码', '基金简称', '近3年', '近2年', '近1年', '今年来']].head(n=10)
fund_by_3year_top10.reset_index(drop=True, inplace=True)
print(fund_by_3year_top10)
print_table_as_image(fund_by_3year_top10, (10, 4), ([0.08, 0.22] + [0.08] * (len(fund_by_3year_top10) - 2)),
                     'fund_by_3year_top10.jpg')

# 基金持股信息
data_name = 'stock_report_fund_hold'
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_report_fund_hold(symbol='基金持仓', date='20210331')
    df.to_pickle(pkl_name)

print(df)
print(df.columns)
print(df.index.size)

# 基金持股Top10
stock_top10 = df[['股票代码', '股票简称', '持有基金家数', '持股总数', '持股市值', '持股变化']].head(n=10)
stock_top10['持股总数'] = stock_top10['持股总数'].astype(float) / 1e8
stock_top10['持股市值'] = stock_top10['持股市值'].astype(float) / 1e8
stock_top10.rename(columns={'持股总数': '持股总数(亿股)', '持股市值': '持股市值(亿元)'}, inplace=True)
print(stock_top10)
print_table_as_image(stock_top10, (12, 4), ([0.1, 0.1, 0.12, 0.16, 0.16, 0.1]),
                     'stock_top10.jpg')
