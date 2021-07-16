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

plt.rcParams['font.size'] = 20

types = ['基金持仓']
years = ['2021', '2020', '2019', '2018']
quarters = ['1231', '0930', '0630', '0331']

for t in types:
    for year in years:
        for q in quarters:
            data_name = 'stock_report_fund_hold({}{}{})'.format(t, year, q)
            pkl_name = '{}.pkl'.format(data_name)
            try:
                df = pd.read_pickle(pkl_name)
            except FileNotFoundError:
                df = ak.stock_report_fund_hold(symbol=t, date='{}{}'.format(year, q))
                if df is None:
                    continue
                df.to_pickle(pkl_name)

            print(t, year, q)
            print(df)
