import datetime as dt
import numpy as np
import pandas as pd
import util as ut

# ****************************************************************************************
# Lagging indicators: 
# 1. Bollinger Bands 
# 2. MACD (Moving Average Convergence Divergence)
# 3. Moving Averages (SMA, EMA)

def sma_indicator(window_sma = 20, input_df = pd.DataFrame()):
    return input_df.rolling(window = window_sma).mean()

def ema_indicator(window_ema = 20, input_df = pd.DataFrame()):
    return input_df.ewm(span = window_ema, adjust = False).mean()

def bb_indicator(window_bb = 20, input_df_close = pd.DataFrame(), input_df_high = pd.DataFrame(), input_df_low = pd.DataFrame()):
    def typical_price_calculation(input_df_close = pd.DataFrame(), input_df_high = pd.DataFrame(), input_df_low = pd.DataFrame()):
        return (input_df_close + input_df_high + input_df_low)/3
    typical_price = typical_price_calculation(input_df_close, input_df_high, input_df_low)
    sma = sma_indicator(window_bb, typical_price)
    std = typical_price.rolling(window = window_bb).std()
    upper_bb = sma + (2 * std)
    lower_bb = sma - (2 * std)
    percent_b = (input_df_close - lower_bb)/(upper_bb - lower_bb)
    return percent_b

def macd_indicator(input_df = pd.DataFrame()):
    return ema_indicator(12, input_df) - ema_indicator(26, input_df)

# ****************************************************************************************
# Leading indicators: 
# 1. PPO (Percentage Price Indicator) ? 
# 2. RSI (Relative Strength Index)
# 3. Stochastic Oscillator
# 4. OBV (On Balance Volume)

def ppo_indicator(input_df = pd.DataFrame()):
    ema_12 = ema_indicator(12, input_df)
    ema_26 = ema_indicator(26, input_df)
    ppo = 100*(ema_12 - ema_26)/(ema_26)
    signalLine = ema_indicator(9, ppo)
    solution = ut.return_triggers(ppo, signalLine)
    return solution

def stch_indicator(input_df_close = pd.DataFrame(), input_df_low = pd.DataFrame(), input_df_high = pd.DataFrame()):
    min_df = input_df_low.rolling(14).min()
    max_df = input_df_high.rolling(14).max()
    percent_k = 100*(input_df_close - min_df)/(max_df - min_df)
    percent_d = sma_indicator(3, percent_k)
    #percent_d crossing above percent_k is a buy signal, percent_d crossing below percent_k is a sell signal
    solution = ut.return_triggers(percent_d, percent_k)
    return solution

def macd_indicator(input_df = pd.DataFrame()):
    return ema_indicator(12, input_df) - ema_indicator(26, input_df)

def rsi_indicator(input_df = pd.DataFrame()):
    delta = input_df.diff() #input_df['adj close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    return (ema_up/ema_down)

# ****************************************************************************************
# Not sure if lagging or leading 

def price_sma_indicator(window_p_sma = 10, input_df = pd.DataFrame()):
    return input_df/sma_indicator(window_p_sma, input_df)

def momentum_indicator(input_df = pd.DataFrame(), window_mom = 10):
    return input_df.pct_change(window_mom)

def price_earnings_indicator(input_df = pd.DataFrame()):
    return "something"


# divergence strategy: 
# Overbought (sell, short) 
# Price/SMA ratio is above > 1.05
# BB% is above > 1.0
# RSI > 70
# Oversold(buy, long)
# Price/SMA ratio is above < .95
# BB% is below < 0
# RSI > 30
# compare with index which might be spydr (this is 
# why it is called divergence strategy)

# def return_triggers(input_df_1 = pd.DataFrame(), input_df_2 = pd.DataFrame()):
#     above_flag = False
#     below_flag = False
#     soln = pd.DataFrame(index = input_df_1.index, columns=['Trigger'])
#     for date in input_df_1.index:
#         if above_flag == False and input_df_1.loc[date,] > input_df_2.loc[date,]:
#             above_flag = True
#         elif above_flag == True and input_df_1.loc[date,] < input_df_2.loc[date,]:
#             soln.at[date,] = -1
#             above_flag = False
#         elif below_flag == False and input_df_1.loc[date,] < input_df_2.loc[date,]:
#             below_flag = True
#         elif below_flag == True and input_df_1.loc[date,] > input_df_2.loc[date,]:  
#             soln.at[date,] = 1
#         else:
#             soln.at[date,] = 0
#     return soln
        

