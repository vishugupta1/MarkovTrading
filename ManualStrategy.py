from re import X
from tkinter import Y
from turtle import color
import util as ut 
import datetime as dt  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import pandas as pd 
import matplotlib.pyplot as plt
import indicators as ind
import numpy as np

def author(self):
    return "vgupta359"

def testPolicy(symbol="IBM", sd=dt.datetime(2009, 1, 1),ed =dt.datetime(2010, 1, 1), sv=10000):  

    dates = pd.date_range(sd, ed)
    symbols = [symbol]

    prices_dataframe = ut.get_data(symbols, dates, False, colname='Adj Close')
    valid_dataframe  = prices_dataframe.dropna()
    valid_dates = valid_dataframe.index
    prices_dataframe = prices_dataframe.dropna()
    #prices_dataframe = prices_dataframe.fillna(method='ffill')
    
    # construct trades vector 
    bb_dataframe = ind.bollinger_bands_indicator(symbol_BB=symbol, sd_bb=sd, ed_bb=ed) 
    trades = pd.DataFrame(index=dates, columns=[symbol+"_Trades"])

    long_amount = 0 
    short_amount = 0 
    above_flag = 0
    below_flag = 0
    for date in trades.index:
        if date not in valid_dates:
            trades.at[date,symbol+"_Trades"] = 0
            continue
        current_trade = 0
        if above_flag == False and bb_dataframe.loc[date, "BB"] > 1:
            above_flag = True
        elif above_flag == True and bb_dataframe.loc[date, "BB"] < 1:
            above_flag = False
            # sell
            if long_amount > 0: 
                current_trade = current_trade - long_amount
                long_amount = 0
            # buy short
            if short_amount == 0:
                short_amount = 1000
                current_trade = current_trade - short_amount
        elif below_flag == False and bb_dataframe.loc[date, "BB"] < 0:
            below_flag = True
        elif below_flag == True and bb_dataframe.loc[date, "BB"] > 0:
            below_flag = False
            # sell short
            if short_amount > 0:
                current_trade = current_trade + short_amount
                short_amount = 0
            # buy
            if long_amount == 0:
                long_amount = 1000
                current_trade = current_trade + long_amount
        trades.at[date,symbol+"_Trades"] = current_trade
    
    #create_charts_MS(symbol=symbol, sd=sd, ed=ed, trades=trades, sv=sv)
    return trades

def generate_plot(x_label = 'x_label', y_label = 'y_label', title_label = 'Title', dataframe = pd.DataFrame(), shorts=[], longs=[]):
    index = 0
    for symbol in dataframe.columns:
        if index == 0:
            plt.plot(dataframe.loc[:,symbol], label=symbol, color='m')  
        else:
            plt.plot(dataframe.loc[:,symbol], label=symbol, color='r')  
        index = index+1
    for i in range(len(shorts)):
        #plt.plot(X=0,Y=shorts[i], color = 'k')
        plt.axvline(x = shorts[i], color = 'k')
    for i in range(len(longs)):
        #plt.plot(X=0,Y=longs[i], color = 'b')
        plt.axvline(x = longs[i], color = 'b')

    plt.gcf().autofmt_xdate()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title_label)
    plt.legend(loc="best")
    plt.grid(True)
    plt.savefig(title_label+'.png')
    plt.clf()

def create_charts_MS(symbol="", sd=dt.datetime(2009, 1, 1),ed=dt.datetime(2010, 1, 1), trades=pd.DataFrame(), sv=100000, title=""):

    benchmark_value = sv
    benchmark_shares = 1000
    dates = pd.date_range(sd, ed)
    symbols = [symbol]
    prices_dataframe = ut.get_data(symbols, dates, False, colname='Adj Close')
    prices_dataframe = prices_dataframe.fillna(method='bfill')
    prices_dataframe = prices_dataframe.fillna(method='ffill')
    portfolio_dataframe = pd.DataFrame(index=dates, columns=[symbol+"_BM", symbol+"_MS"])

    # construct portfolio valuation for benchmark 
    benchmark_initial_price = prices_dataframe.iloc[0, 0]
    benchmark_cost = benchmark_initial_price * benchmark_shares
    benchmark_value = benchmark_value - benchmark_cost
    for date in dates:
        benchmark_current_price = prices_dataframe.loc[date, symbol]
        portfolio_dataframe.at[date, symbol+"_BM"] = benchmark_value + benchmark_shares*benchmark_current_price

    # construct portfolio valuation for manual strategy
    cash_value = 100000
    short_amount = 0
    long_amount = 0
    initial_short_price = 0
    current_trade_amount = 0
    shorts = []
    longs = []
    for date in dates:
        current_trade = trades.loc[date, symbol+"_Trades"]
        current_price = prices_dataframe.loc[date, symbol]
        current_trade_amount = current_trade_amount + current_trade
        if current_trade == 1000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
            longs.append(date)
        if current_trade == 2000:
            long_amount = 1000
            cash_value = cash_value - (current_price*1000)
            short_value = (short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price))
            cash_value = cash_value + short_value
            short_amount = 0
            longs.append(date)
        if current_trade == -1000:
            short_amount = 1000
            cash_value = cash_value - (current_price*1000)
            initial_short_price = current_price
            shorts.append(date)
        if current_trade == -2000:
            long_amount = 0
            cash_value = cash_value - (current_price*1000)
            cash_value = cash_value + (current_price*1000)
            short_amount = 1000
            initial_short_price = current_price
            shorts.append(date)
        portfolio_dataframe.at[date, symbol+"_MS"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))
        
    # normalize and statistics 
    portfolio_dataframe.loc[:, symbol+"_BM"] = portfolio_dataframe.loc[:, symbol+"_BM"]/portfolio_dataframe.loc[sd, symbol+"_BM"]
    portfolio_dataframe.loc[:, symbol+"_MS"] = portfolio_dataframe.loc[:, symbol+"_MS"]/portfolio_dataframe.loc[sd, symbol+"_MS"]
    cumulative_return_symbol = (portfolio_dataframe.loc[ed, symbol + "_MS"] - portfolio_dataframe.loc[sd, symbol + "_MS"])/portfolio_dataframe.loc[sd, symbol + "_MS"]
    cumulative_return_BenchMark = (portfolio_dataframe.loc[ed,symbol + "_BM"] - portfolio_dataframe.loc[sd, symbol + "_BM"])/portfolio_dataframe.loc[sd, symbol + "_BM"]
    std_symbol = portfolio_dataframe[symbol + "_MS"].std()
    std_BenchMark = portfolio_dataframe[symbol + "_BM"].std()
    mean_symbol = portfolio_dataframe[symbol + "_MS"].mean()
    mean_BenchMark = portfolio_dataframe[symbol + "_BM"].mean()
    print("Cumulative return " + str(symbol + "_MS") + ": " + str(cumulative_return_symbol))
    print("Cumulative return " + str(symbol + "_BM") + ": " + str(cumulative_return_BenchMark))
    print("STD " + str(symbol + "_MS") + ": " + str(std_symbol))
    print("STD " + str(symbol + "_BM") + ": " + str(std_BenchMark))
    print("Mean " + str(symbol + "_MS") + ": " + str(mean_symbol))
    print("Mean " + str(symbol + "_BM") + ": " + str(mean_BenchMark))
    
    generate_plot(x_label = "Dates", y_label="Prices", title_label=title,dataframe=portfolio_dataframe, longs=longs, shorts=shorts)






