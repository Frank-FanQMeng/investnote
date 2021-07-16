# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt


def plot_report(data, x, y, z, name):
    ax = data.pivot(x, y, z).plot.bar(figsize=(12, 4), rot=0)
    ax.text(0.5, 0.5, '老涂数据投研(py_invest_note)', transform=ax.transAxes,
            fontsize=28, color='gray', alpha=0.5,
            ha='center', va='center', rotation='30')
    plt.title('{}{}'.format(name, z))
    plt.savefig('{}({}).jpg'.format(name, z), bbox_inches='tight')


# 调整输出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

plt.rcParams['font.size'] = 20

code = '600066'
s_name = '宇通客车'

data_name = 'stock_financial_analysis_indicator({})'.format(code)
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_financial_analysis_indicator(stock=code)
    df.to_pickle(pkl_name)

print(df.dtypes)
print(df)

reports = ['资产负债表', '利润表', '现金流量表']

report = reports[0]
data_name = 'stock_financial_report_sina({})_{}'.format(code, report)
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_financial_report_sina(stock=code, symbol=report)
    df.to_pickle(pkl_name)

print(report)
df = df[['报表日期', '流动资产合计', '应收票据及应收账款', '存货', '非流动资产合计', '资产总计', '流动负债合计', '非流动负债合计', '负债合计']]
num_cols = df.columns.drop('报表日期')
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce').apply(lambda x: x / 1e8)
df.insert(1, '年', df['报表日期'].apply(lambda x: int(x[:4])))
df.insert(2, '月', df['报表日期'].apply(lambda x: x[4:6]))
df = df[df['年'].isin([2021, 2020, 2019, 2018, 2017])]
print(df.dtypes)
print(df)
plot_report(df, '年', '月', '资产总计', s_name)
plot_report(df, '年', '月', '负债合计', s_name)

report = reports[1]
data_name = 'stock_financial_report_sina({})_{}'.format(code, report)
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_financial_report_sina(stock=code, symbol=report)
    df.to_pickle(pkl_name)

print(report)
df = df[['报表日期', '一、营业总收入', '二、营业总成本', '销售费用', '研发费用', '五、净利润']]
num_cols = df.columns.drop('报表日期')
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce').apply(lambda x: x / 1e8)
df.insert(1, '年', df['报表日期'].apply(lambda x: int(x[:4])))
df.insert(2, '月', df['报表日期'].apply(lambda x: x[4:6]))
df = df[df['年'].isin([2021, 2020, 2019, 2018, 2017])]
print(df.dtypes)
print(df)
for col in num_cols.tolist():
    plot_report(df, '月', '年', col, s_name)

report = reports[2]
data_name = 'stock_financial_report_sina({})_{}'.format(code, report)
pkl_name = '{}.pkl'.format(data_name)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_financial_report_sina(stock=code, symbol=report)
    df.to_pickle(pkl_name)

print(report)
df = df[['报表日期', '经营活动现金流入小计', '经营活动现金流出小计', '经营活动产生的现金流量净额']]
num_cols = df.columns.drop('报表日期')
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce').apply(lambda x: x / 1e8)
df.insert(1, '年', df['报表日期'].apply(lambda x: int(x[:4])))
df.insert(2, '月', df['报表日期'].apply(lambda x: x[4:6]))
df = df[df['年'].isin([2021, 2020, 2019, 2018, 2017])]
print(df.dtypes)
print(df)
for col in num_cols.tolist():
    plot_report(df, '月', '年', col, s_name)
