import datetime as dt
import pandas as pd
import ManualStrategy as ms
import StrategyLearner as sl
import util as ut
import matplotlib.pyplot as plt

def generate_plot(x_label = 'x_label', y_label = 'y_label', title_label = 'Title', dataframe = pd.DataFrame(), shorts=[], longs=[]):
    index = 0
    for symbol in dataframe.columns:
        plt.plot(dataframe.loc[:,symbol], label=symbol) 
    
    for i in range(len(shorts)):
        plt.axvline(x = shorts[i], color = 'black')
    for i in range(len(longs)):
        plt.axvline(x = longs[i], color = 'blue')

    plt.gcf().autofmt_xdate()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title_label)
    plt.legend(loc="best")
    plt.savefig(title_label+'.png')
    plt.clf()


def perform_experiment_2(symbol="", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=100000, title=""):
   
    sl_learner = sl.StrategyLearner(impact=0.005)
    sl_learner.add_evidence(symbol=symbol, sd=sd,ed=ed, sv=100000)
    trades_sl = sl_learner.testPolicy(symbol=symbol, sd=sd,ed=ed, sv=100000)

    sl_learner2 = sl.StrategyLearner(impact=0.05)
    sl_learner2.add_evidence(symbol=symbol, sd=sd,ed=ed, sv=100000)
    trades_sl2 = sl_learner2.testPolicy(symbol=symbol, sd=sd,ed=ed, sv=100000)

    sl_learner3 = sl.StrategyLearner(impact=.5)
    sl_learner3.add_evidence(symbol=symbol, sd=sd,ed=ed, sv=100000)
    trades_sl3 = sl_learner3.testPolicy(symbol=symbol, sd=sd,ed=ed, sv=100000)

    
    dates = pd.date_range(sd, ed)
    prices_dataframe = ut.get_data(symbols=[symbol], dates=dates, addSPY=False, colname="Adj Close")
    prices_dataframe = prices_dataframe.fillna(method='bfill')
    prices_dataframe = prices_dataframe.fillna(method='ffill')
    portfolio_dataframe = pd.DataFrame(index=dates, columns=[symbol+"_SL1",symbol+"_SL2",symbol+"_SL3"])

    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    for date in dates:
        current_trade = trades_sl.loc[date, symbol+"_Trades"]
        current_price = prices_dataframe.loc[date, symbol]
        current_trade_amount = current_trade_amount + current_trade
        if current_trade == 1000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
        if current_trade == 2000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
            short_value = (short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price))
            cash_value = cash_value + short_value
            short_amount = 0
        if current_trade == -1000:
            short_amount = 1000
            cash_value = cash_value - (current_price*1000)
            initial_short_price = current_price
        if current_trade == -2000:
            long_amount = 0
            cash_value = cash_value - (current_price*1000)
            cash_value = cash_value + (current_price*1000)
            short_amount = 1000
            initial_short_price = current_price
        portfolio_dataframe.at[date, symbol+"_SL1"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))

    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    for date in dates:
        current_trade = trades_sl2.loc[date, symbol+"_Trades"]
        current_price = prices_dataframe.loc[date, symbol]
        current_trade_amount = current_trade_amount + current_trade
        if current_trade == 1000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
        if current_trade == 2000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
            short_value = (short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price))
            cash_value = cash_value + short_value
            short_amount = 0
        if current_trade == -1000:
            short_amount = 1000
            cash_value = cash_value - (current_price*1000)
            initial_short_price = current_price
        if current_trade == -2000:
            long_amount = 0
            cash_value = cash_value - (current_price*1000)
            cash_value = cash_value + (current_price*1000)
            short_amount = 1000
            initial_short_price = current_price
        portfolio_dataframe.at[date, symbol+"_SL2"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))

    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    for date in dates:
        current_trade = trades_sl3.loc[date, symbol+"_Trades"]
        current_price = prices_dataframe.loc[date, symbol]
        current_trade_amount = current_trade_amount + current_trade
        if current_trade == 1000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
        if current_trade == 2000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
            short_value = (short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price))
            cash_value = cash_value + short_value
            short_amount = 0
        if current_trade == -1000:
            short_amount = 1000
            cash_value = cash_value - (current_price*1000)
            initial_short_price = current_price
        if current_trade == -2000:
            long_amount = 0
            cash_value = cash_value - (current_price*1000)
            cash_value = cash_value + (current_price*1000)
            short_amount = 1000
            initial_short_price = current_price
        portfolio_dataframe.at[date, symbol+"_SL3"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))
    
    portfolio_dataframe.loc[:, symbol+"_SL1"] = portfolio_dataframe.loc[:, symbol+"_SL1"]/portfolio_dataframe.loc[sd, symbol+"_SL1"]
    portfolio_dataframe.loc[:, symbol+"_SL2"] = portfolio_dataframe.loc[:, symbol+"_SL2"]/portfolio_dataframe.loc[sd, symbol+"_SL2"]
    portfolio_dataframe.loc[:, symbol+"_SL3"] = portfolio_dataframe.loc[:, symbol+"_SL3"]/portfolio_dataframe.loc[sd, symbol+"_SL3"]
    generate_plot(x_label = "Dates", y_label="Prices", title_label=title,dataframe=portfolio_dataframe)

def main():
    perform_experiment_2(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=100000, title="Experiment2_Portfolio_In_Sample") # insample
    perform_experiment_2(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 1, 1), sv=100000, title="Experiment2_Portfolio_Out_Sample") # outsample



