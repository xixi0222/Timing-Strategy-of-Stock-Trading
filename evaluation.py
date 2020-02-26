import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import xlwt 

plt.style.use('seaborn')

def evaluation(trans, data):
    """
    Function: Financial evaluation: Sharpe ratio, Annual simple return, Win rate, \
              Maximum drawdown, Maximum loss rate, Transactions frequency...
              Visualization and output of data.

    Parameters:
    trans: transaction record
    data: stock and trading data
    """
    # number of trading days approximately in one year
    N = 250

    # Annual simple return
    ret_y = data.PnL[data.shape[0] - 1]**(N / data.shape[0]) - 1
    
    # Sharpe Ratio
    Sharpe_ratio = (data.simple_return * data.position).mean() / \
                   (data.simple_return * data.position).std() * np.sqrt(data.shape[0])
    
    # win rate
    win_ratio = ((trans.price_sell - trans.price_buy) > 0).mean()

    # Get drawdown and maximum drawdown
    drawdown = 1 - data.PnL / data.PnL.cummax()
    max_drawdown = max(drawdown)

    # get maximum loss rate
    max_loss = min(trans.price_sell / trans.price_buy - 1)
    
    # Evaluation per year
    data['year'] = data.DateTime.apply(lambda x: x[:4])
    PnL_per_year = data.PnL.groupby(data.year).last() / data.PnL.groupby(data.year).first() - 1
    benchmark_per_year = data.benchmark.groupby(data.year).last()/data.benchmark.groupby(data.year).first() - 1
    
    excess_ret = PnL_per_year - benchmark_per_year
    result_per_year = pd.concat([PnL_per_year,benchmark_per_year,excess_ret], axis = 1)
    result_per_year.columns = ['Simple return','Benchmark return','Excess return']
    result_per_year = result_per_year.T
    
    # Draw diagrams 
    xtick = np.round(np.linspace(0, data.shape[0] - 1, 7), 0)
    xticklabel = data.DateTime[xtick]
    
    ax1 = plt.axes()
    plt.plot(np.arange(data.shape[0]), data.benchmark, 'black', label = 'Benchmark', linewidth = 2)
    plt.plot(np.arange(data.shape[0]), data.PnL, 'red', label = 'PnL', linewidth = 2)
    plt.plot(np.arange(data.shape[0]), data.PnL / data.benchmark, 'orange', label = 'Relative Yield', linewidth = 2)

    plt.legend()
    ax1.set_xticks(xtick) # choose x tick positions
    ax1.set_xticklabels(xticklabel) # assign labels on x tick positions
    plt.savefig('return.jpg')

    print('-' * 100)
    print('Sharpe ratio: ',round(Sharpe_ratio, 2))
    print('Annual simple return: {}%'.format(round(ret_y * 100, 2)))
    print('Win rate：{}%'.format(round(win_ratio * 100, 5)))
    print('Maximum drawdown：{}%'.format(round(max_drawdown * 100, 2)))
    print('Maximum loss rate: {}%'.format(round(-max_loss * 100,2)))
    print('Number of transactions with monthly frequency: {} (Buy and sell in total)'.\
          format(round(data.flag.abs().sum() / data.shape[0]*20,2)))
    
    result = {'Sharp': Sharpe_ratio,
              'Ret_y': ret_y,
              'Win_rate': win_ratio,
              'MDD': max_drawdown,
              'Max_loss_rate': -max_loss,
              'Trade_rate': round(data.flag.abs().sum() / data.shape[0], 1)}
    
    result = pd.DataFrame.from_dict(result, orient='index').T

    result_per_year.T.plot()
    plt.title('Return')
    plt.xlabel('Year')
    plt.ylabel('Simple return')
    plt.savefig('return_per_year.jpg')

    print('-' * 100)
    print(result)
    print('-' * 100)
    print(result_per_year)
    
    return result, result_per_year
