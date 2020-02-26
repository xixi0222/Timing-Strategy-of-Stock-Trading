import pandas as pd
from market_timing import timing_strategy



if __name__ == '__main__':
    data = pd.read_csv('CSI300.csv', encoding = 'gbk')
    
    win_short = 4
    win_long = 7
    stats, result_per_year, pd_transactions, data = timing_strategy(data, win_long, win_short, loss_ratio=0.01)
    