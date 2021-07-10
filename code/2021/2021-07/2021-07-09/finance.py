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
pd.set_option('display.max_rows', None)

plt.rcParams['font.size'] = 20

zh_names = '格力电器 爱尔眼科 宁德时代'.split(' ')
s_codes = ['000651', '300015', '300750']

for name, code in zip(zh_names, s_codes):
    data_name = 'stock_financial_abstract({})'.format(code)
    pkl_name = '{}.pkl'.format(data_name)
    try:
        df = pd.read_pickle(pkl_name)
    except FileNotFoundError:
        df = ak.stock_financial_abstract(stock=code)
        df.to_pickle(pkl_name)

    df.drop(columns=['每股净资产-摊薄/期末股数', '每股现金流', '每股资本公积金', '固定资产合计', '流动资产合计', '长期负债合计', '财务费用'], axis=1, inplace=True)

    df['资产总计'] = df['资产总计'] \
        .apply(lambda x: x if isinstance(x, float) else float(x.replace(',', '').replace('元', '')) / 1e8)
    df['主营业务收入'] = df['主营业务收入'] \
        .apply(lambda x: x if isinstance(x, float) else float(x.replace(',', '').replace('元', '')) / 1e8)
    df['净利润'] = df['净利润'] \
        .apply(lambda x: x if isinstance(x, float) else float(x.replace(',', '').replace('元', '')) / 1e8)
    df.insert(1, '年', df['截止日期'].apply(lambda x: int(x[:4])))
    df.insert(2, '月', df['截止日期'].apply(lambda x: x[5:7]))
    df = df[df['年'].isin([2021, 2020, 2019, 2018, 2017])]
    print(name)

    print_table_as_image(df.head(n=5), fig_size=(10, 2),
                         col_width=[0.1] * 6,
                         image_name='{}_净利润表.jpg'.format(name))

    df['营业收入增速'] = float('NaN')
    df['净利润增速'] = float('NaN')
    # print(df)
    for ind, row in df.iterrows():
        year = row['年']
        month = row['月']
        income = row['主营业务收入']
        profit = row['净利润']
        last_row = df.loc[(df['年'] == year - 1) & (df['月'] == month)]  # DataFrame
        if last_row.empty:
            continue
        last_income = last_row['主营业务收入'].iloc[0]
        last_profit = last_row['净利润'].iloc[0]
        df.loc[ind, '营业收入增速'] = (income - last_income) / income * 100
        df.loc[ind, '净利润增速'] = (profit - last_profit) / profit * 100

    print(df)

    for col in ['主营业务收入', '净利润', '营业收入增速', '净利润增速']:
        a = df.pivot('月', '年', col).plot.bar(figsize=(16, 9), rot=0)
        a.text(0.5, 0.5, '老涂数据投研(py_invest_note)', transform=a.transAxes,
               fontsize=28, color='gray', alpha=0.5,
               ha='center', va='center', rotation='30')
        plt.title('近5年{}-{}对比'.format(name, col))
        plt.savefig('{}_{}.jpg'.format(name, col), bbox_inches='tight')
