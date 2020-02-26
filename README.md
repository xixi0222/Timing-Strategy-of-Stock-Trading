### Timing Strategy of Stock Trading 择时股票指数交易

#### Brief Introduction
* Stock trading using timing strategy: mainly use short & long moving average of stock price and also analyze the performance of this strategy.

#### Algorithm pipeline
1. Compute **short & long moving average** of stock price. 
2. Use the infomation of moving average to trade the index. 
3. Record and compute data of buy & sell, position, return, etc. with daily frequency for later analysis. 
4. Do financial evaluation: Sharpe ratio, Annual simple return, Win rate, Maximum drawdown, Maximum loss rate, Transaction frequency...
5. Visualization and output of data.

#### Strategy Details
* Long (Buy)
    * No position currently;
    * Short moving average line crosses long moving average line upward.
* Short (Sell)
    * Hold full position currently;
    * Return is below stop loss ratio.
* Short (Sell)
    * Full position currently;
    * Short moving average line crosses long ma line downward.
* Position remains unchanged
    * Default.

#### Results
1. Sharpe ratio:  1.47
2. Annual simple return: 4.52%
3. Win rate：50.92025%
4. Maximum drawdown：25.62%
5. Maximum loss rate: 6.94%
6. Trade frequency: 10%
7. Other diagrams and Excel file are in this folder for your reference.

#### Data
1. Trading target: CSI300 Index. 
2. Time length: Year 2010 - Year 2019.
3. Data Source: *Wind*

