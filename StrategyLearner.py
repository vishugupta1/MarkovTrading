import datetime as dt  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import random
from tkinter.tix import Tree
from matplotlib.pyplot import axis  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import numpy as np		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import pandas as pd
import indicators as ind		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import util as ut  	
import BagLearner as bl	  	
import RTLearner as rt   
import ImportData as ID		

def author(self):
    return "vgupta359"
  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
class StrategyLearner(object):  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        self.verbose = verbose  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        self.impact = impact  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        self.commission = commission
   
    def add_evidence(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=10000):  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	
        # dates = pd.date_range(sd, ed)
        # prices_dataframe = ut.get_data(symbols=[symbol], dates=dates, addSPY=False, colname="Adj Close")
        # prices_dataframe = prices_dataframe.dropna()

        # import stock(s) data
        stocks_data = pd.DataFrame()
        stocks_data = ID.get_stock_data(symbol, sd, ed)
       
        # technical analysis
        training_data = pd.DataFrame(index=stocks_data.index, columns=['SMA', 'EMA', 'BB', 'MACD', 'PPO', 'STCH', 'RSI', 'P/SMA', 'MOM', 'P/E'])  	
        training_data.at[:, 'SMA'] = ind.sma_indicator(20, stocks_data.loc[:, 'Adj Close'])
        training_data.at[:, 'EMA'] = ind.ema_indicator(20, stocks_data.loc[:, 'Adj Close'])
        training_data.at[:, 'BB'] = ind.bb_indicator(20, stocks_data.loc[:, 'Adj Close'], stocks_data.loc[:, 'High'], stocks_data.loc[:, 'Low'])
        training_data.at[:, 'MACD'] = ind.macd_indicator(stocks_data.loc[:, 'Adj Close'])
        #training_data.at[:, 'PPO'] = ind.ppo_indicator(stocks_data.loc[:, 'Adj Close'])
        #training_data.at[:, 'STCH'] = ind.stch_indicator(stocks_data.loc[:, 'Adj Close'], stocks_data.loc[:, 'Low'], stocks_data.loc[:, 'High'])
        training_data.at[:, 'RSI'] = ind.rsi_indicator(stocks_data.loc[:, 'Adj Close'])
        training_data.at[:, 'P/SMA'] = ind.price_sma_indicator(10, stocks_data.loc[:, 'Adj Close'])
        training_data.at[:, 'MOM'] = ind.momentum_indicator(stocks_data.loc[:, 'Adj Close'])
        #training_data.at[:, 'P/E'] = ind.price_earnings_indicator(stocks_data.loc[:, 'Adj Close'])

        print(training_data)
        return

        # construct Y_Value Vector
        y_buy_threshold = 5 #percent
        y_sell_threshold = -5 #percent
        n_day = 5 #day of return
        modified_prices_dataframe = prices_dataframe
        modified_prices_dataframe=modified_prices_dataframe.reset_index()
        index = 0
        for date in prices_dataframe.index:
            if index+N_Day > training_data.shape[0]-1:
                training_data.at[date,"Y_Value"] = 0
                continue
            return_value = ((modified_prices_dataframe.loc[index+N_Day, symbol]/modified_prices_dataframe.loc[index,symbol])-1.0)*100
            if return_value > Y_Buy:
                training_data.at[date,"Y_Value"] = 1
            elif return_value < Y_Sell:
                training_data.at[date,"Y_Value"] = -1
            else:
                training_data.at[date,"Y_Value"] = 0
            index = index+1
        
        Xtrain = training_data.iloc[:, 0:-2]
        Ytrain = training_data.iloc[:, -1]
        Xtrain = Xtrain.to_numpy()
        Ytrain = Ytrain.to_numpy()

        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {'leaf_size':5}, bags = 20, boost = False, verbose = False)
        self.learner.add_evidence(Xtrain, Ytrain)
	  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 


    def testPolicy(  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        self,  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        symbol="IBM",  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        sd=dt.datetime(2009, 1, 1),  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        ed=dt.datetime(2010, 1, 1),  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        sv=10000,  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    ):  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

        dates = pd.date_range(sd, ed)
        prices_dataframe = ut.get_data(symbols=[symbol], dates=dates, addSPY=False, colname="Adj Close")
        valid_dataframe  = prices_dataframe.dropna()
        valid_dates = valid_dataframe.index
        #print(valid_dates)
        prices_dataframe = prices_dataframe.dropna()

        testing_data = pd.DataFrame(index=prices_dataframe.index, columns=[symbol+"_BB", symbol+"_PPO", symbol+"_Stch", symbol+"_MOM", symbol + "_MACD"])  	
        bb_dataframe = ind.bollinger_bands_indicator(symbol_BB=symbol, sd_bb=sd, ed_bb=ed) 
        ppo_dataframe = ind.percentage_price_indicator(symbol_ppo=symbol,sd_ppo=sd, ed_ppo=ed) 
        stch_dataframe = ind.stochastic_indicator(symbol_stch=symbol,sd_stch=sd, ed_stch=ed) 
        mom_dataframe = ind.momentum_indicator(symbol_mom=symbol, input_window_mom=5, sd_mom=sd, ed_mom=ed)
        macd_dataframe = ind.macd_indicator(symbol_macd=symbol, sd_macd=sd, ed_macd=ed)

        testing_data.at[:, symbol+"_BB"] = bb_dataframe.loc[:, "BB"]
        testing_data.at[:, symbol+"_PPO"] = ppo_dataframe.loc[:, "PPO"]
        testing_data.at[:, symbol+"_Stch"] = stch_dataframe.loc[:, "STCH"]
        testing_data.at[:, symbol+"_MOM"] = mom_dataframe.loc[:, "MOM"]
        testing_data.at[:, symbol+"_MACD"] = macd_dataframe.loc[:, "MACD"]

        Y_Value = self.learner.query(Xtest=testing_data.to_numpy())
        trades = pd.DataFrame(index=dates, columns=[symbol+"_Trades"])
        #portfolio_dataframe = pd.DataFrame(index=prices_dataframe.index, columns=[symbol+"_BM",])

        long_amount = 0 
        short_amount = 0 
        initial_short_price = 0
        cash_value = sv
        index = 0
        for date in dates:
            current_price = prices_dataframe.loc[date,symbol]
            current_trade = 0
            if date not in valid_dates:
                trades.at[date,symbol+"_Trades"] = 0
                continue
            if Y_Value[index] - self.impact < 0:
                # sell
                if long_amount > 0: 
                    sell_value = long_amount * current_price
                    cash_value = cash_value + sell_value - (sell_value)*self.impact
                    current_trade = current_trade - long_amount
                    long_amount = 0
                # buy short
                if short_amount == 0:
                    short_amount = 1000
                    initial_short_price = current_price
                    cash_value = cash_value - (short_amount*current_price) - (short_amount*current_price)*self.impact
                    current_trade = current_trade - short_amount
            elif Y_Value[index] - self.impact > 0:
                # sell short
                if short_amount > 0:
                    sell_value = (short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price))
                    cash_value = cash_value + sell_value - (short_amount*current_price)*self.impact
                    current_trade = current_trade + short_amount
                    short_amount = 0
                # buy
                if long_amount == 0:
                    long_amount = 1000
                    cash_value = cash_value - (long_amount*current_price) - (long_amount*current_price)*self.impact
                    current_trade = current_trade + long_amount
           
            #portfolio_dataframe.at[date, symbol + "_SL"] = cash_value + (current_price*long_amount) + ((short_amount*initial_short_price)-(short_amount*(current_price-initial_short_price)))
            trades.at[date,symbol+"_Trades"] = current_trade
            index = index + 1
        return trades

if __name__ == '__main__':
    SL = StrategyLearner()
    SL.add_evidence()
    

 			 	 	 		 		 	 		 		 	 		  	 	 			  	 