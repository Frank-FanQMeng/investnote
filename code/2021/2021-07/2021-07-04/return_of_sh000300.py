# @Site   :  https://github.com/pynote/investnote
# @Author :  老涂数据投研(py_invest_note)

import os.path
import math
import pandas as pd
from pandas import Timestamp
import matplotlib.pyplot as plt
import akshare as ak
from dateutil import relativedelta

# data
s_code = 'sh000300'
pkl_name = '{}.pkl'.format(s_code)
try:
    df = pd.read_pickle(pkl_name)
except FileNotFoundError:
    df = ak.stock_zh_index_daily(s_code)
    df.to_pickle(pkl_name)

print(df)


# df['close'].plot()
# plt.show()


def calc_annual_rate_of_return(data, start_date, end_date):
    """
    计算一次性投入年化收益率
    """
    print(f'{start_date=}')
    print(f'{end_date=}')
    time_span = relativedelta.relativedelta(end_date, start_date)
    years = time_span.years + time_span.months / 12
    print(f'{years=}')
    start_price = data['close'][start_date]
    end_price = data['close'][end_date]
    multi = end_price / start_price
    print(f'{start_price=}')
    print(f'{end_price=}')
    print(f'{multi=}')
    annual_rate_of_return = math.exp(math.log(multi) / years) - 1
    print(f'{annual_rate_of_return=}')


def calc_average_annual_rate_of_return(data, start_date, end_date, span=7):
    """
    计算定投年化收益率
    """
    print(f'{start_date=}')
    print(f'{end_date=}')
    time_span = relativedelta.relativedelta(end_date, start_date)
    years = time_span.years + time_span.months / 12
    print(f'{years=}')
    start_loc = data.index.get_loc(start_date)
    end_loc = data.index.get_loc(end_date)
    average = 0
    count = 0
    for i in range(start_loc, end_loc, span):
        average += 1 / data['close'][i]
        count += 1
    print(f'{count=}')
    average_price = count / average
    end_price = data['close'][end_date]
    multi = end_price / average_price
    print(f'{average_price=}')
    print(f'{end_price=}')
    print(f'{multi=}')
    print(f'{multi*count=}')
    average_annual_rate_of_return = math.exp(math.log(multi) / years) - 1
    print(f'{average_annual_rate_of_return=}')
    plt.rcParams.update({'font.size': 24})
    data = data[start_date:end_date]
    data['close'].plot(figsize=(16, 9))
    average_data = pd.DataFrame(index=data.index.copy())
    average_data.insert(0, 'average_price', [average_price] * data.index.size)
    average_data['average_price'].plot()
    # plt.show()
    plt.savefig(fname='{}.jpg'.format(os.path.splitext(os.path.basename(__file__))[0]))


# 一次性定投
s_date = Timestamp('2016-01-27 00:00:00+00:00')
e_date = df.index[-1]
calc_annual_rate_of_return(df, s_date, e_date)

s_date = Timestamp('2019-01-03 00:00:00+00:00')
e_date = df.index[-1]
calc_annual_rate_of_return(df, s_date, e_date)

# 每周定投
s_date = Timestamp('2015-06-08 00:00:00+00:00')
e_date = df.index[-1]
calc_average_annual_rate_of_return(df, s_date, e_date)
