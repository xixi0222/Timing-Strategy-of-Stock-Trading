import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import xlwt
from evaluation import evaluation

plt.style.use('seaborn')

def timing_strategy(price_data, win_short, win_long, loss_ratio=0.1):
    """
    Function: Compute short and long moving average of stock price. Use 
    the infomation of moving average to do the trading. Also, record and 
    compute date of buy & sell, position, return, etc. with daily frequency 
    for later analysis.

    Parameters:
    price_data: stock price sequence
    win_short: window length for computing short moving average of price
    win_long: window length for computing long moving average of price
    loss_ratio：stop loss ratio. Default: 10%.
    """

    data = price_data.copy()

    data['sma'] = data.CLOSE.rolling(win_short, min_periods = 0).mean()
    data['lma'] = data.CLOSE.rolling(win_long, min_periods = 0).mean()
    
    # Record position: 0 / 1
    data['position'] = 0
    # Record buy/sell: 1 / -1 
    data['flag'] = 0 
    
    record_buy = []
    record_sell = []
    price_in = 0
    len_days = data.shape[0] - 1
    for i in range(win_long, len_days):

        # 1. No position currently; 2. Short moving average line crosses long ma line upward.
        # 1 & 2 => Long (Buy)
        if (data.sma[i - 1] < data.lma[i - 1]) and (data.sma[i] > data.lma[i]) and (data.position[i] == 0):
            data.loc[i,'flag'] = 1
            data.loc[i + 1,'position'] = 1
            date_in = data.DateTime[i]
            price_in = data.loc[i,'CLOSE']
            record_buy.append([date_in, price_in])

        # 1. Hold full position currently; 2. Return is below stop loss ratio.
        # 1 & 2 => Short (Sell)
        elif (data.position[i] == 1) and (data.CLOSE[i] / price_in - 1 < - loss_ratio):
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0            
            record_sell.append([data.DateTime[i], data.loc[i, 'CLOSE']])

        # 1. Full position currently; 2. Short moving average line crosses long ma line downward.
        # 1 & 2 => Short (Sell)
        elif  (data.sma[i-1] > data.lma[i-1]) and (data.sma[i] < data.lma[i]) and (data.position[i] == 1):
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0  
            record_sell.append([data.DateTime[i], data.loc[i, 'CLOSE']])
            
        # Default: Position remains unchanged.
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    pd_buy = pd.DataFrame(record_buy, columns = ['date_buy','price_buy'])
    pd_sell = pd.DataFrame(record_sell, columns = ['date_sell','price_sell'])
    pd_transactions = pd.concat([pd_buy, pd_sell], axis = 1)
            
    data = data.loc[win_long:, :].reset_index(drop = True)
    data['simple_return'] = data.CLOSE.pct_change(1).fillna(0)
    data['PnL'] = (1 + data.simple_return * data.position).cumprod()
    data['benchmark'] = data.CLOSE / data.CLOSE[0]

    stats, result_per_year = evaluation(pd_transactions, data)

    # Output into Excel
    with pd.ExcelWriter("trade_record.xlsx") as writer:
        data.to_excel(writer, sheet_name='stock_data')
        pd_transactions.to_excel(writer, sheet_name='trade_record')
        stats.to_excel(writer, sheet_name='overall_stats')
        result_per_year.to_excel(writer, sheet_name='return_per_year')

    return stats, result_per_year, pd_transactions, data
    
    
    
    
    

