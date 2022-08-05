from mimetypes import init
import ManualStrategy as ms
import StrategyLearner as sl
import datetime as dt
import util as ut
import pandas as pd
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


def perform_experiment_1(symbol="", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=100000, title=""):
   
    trades_ms = ms.testPolicy(symbol="JPM", sd=sd,ed =ed, sv=100000)
    sl_learner = sl.StrategyLearner()
    sl_learner.add_evidence(symbol=symbol, sd=sd,ed=ed, sv=100000)
    trades_sl = sl_learner.testPolicy(symbol=symbol, sd=sd,ed=ed, sv=100000)

    
    dates = pd.date_range(sd, ed)
    prices_dataframe = ut.get_data(symbols=[symbol], dates=dates, addSPY=False, colname="Adj Close")
    prices_dataframe = prices_dataframe.fillna(method='bfill')
    prices_dataframe = prices_dataframe.fillna(method='ffill')
    portfolio_dataframe = pd.DataFrame(index=prices_dataframe.index, columns=[symbol+"_BM",symbol+"_MS",symbol+"_SL"])



    # **********************************************************************************************************************
    benchmark_value = 100000
    benchmark_shares = 1000
    benchmark_initial_price = prices_dataframe.iloc[0, 0]
    benchmark_cost = benchmark_initial_price * benchmark_shares
    benchmark_value = benchmark_value - benchmark_cost
    for date in prices_dataframe.index:
        benchmark_current_price = prices_dataframe.loc[date, symbol]
        portfolio_dataframe.at[date, symbol+"_BM"] = benchmark_value + benchmark_shares*benchmark_current_price
   
    # **********************************************************************************************************************
    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    for date in prices_dataframe.index:
        current_trade = trades_ms.loc[date, symbol+"_Trades"]
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

        portfolio_dataframe.at[date, symbol+"_MS"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))
   
    # **********************************************************************************************************************
    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    for date in prices_dataframe.index:
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

        portfolio_dataframe.at[date, symbol+"_SL"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))
    
    portfolio_dataframe.loc[:, symbol+"_SL"] = portfolio_dataframe.loc[:, symbol+"_SL"]/portfolio_dataframe.loc[sd, symbol+"_SL"]
    portfolio_dataframe.loc[:, symbol+"_MS"] = portfolio_dataframe.loc[:, symbol+"_MS"]/portfolio_dataframe.loc[sd, symbol+"_MS"]
    portfolio_dataframe.loc[:, symbol+"_BM"] = portfolio_dataframe.loc[:, symbol+"_BM"]/portfolio_dataframe.loc[sd, symbol+"_BM"]
  
    generate_plot(x_label = "Dates", y_label="Prices", title_label=title,dataframe=portfolio_dataframe)



def main():
    perform_experiment_1(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=100000, title="Experiment1_Portfolio_In_Sample") # insample
    perform_experiment_1(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 1, 1), sv=100000, title="Experiment1_Portfolio_Out_Sample") # outsample









    











