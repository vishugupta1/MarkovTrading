
from distutils.command.sdist import sdist
from tracemalloc import start
# import robin_stocks.robinhood as rh
# import pyotp
import yfinance as yf
import datetime as dt
import pandas as pd


def get_stock_data(symbols = '', sd = '', ed = ''):
    return pd.DataFrame(yf.download(symbols, sd, ed))


if __name__ == "__main__":
    start_date = '1990-01-01'
    end_date = '2021-07-12'
    ticker = ['AMZN', 'TSLA']
    get_stock_data('AMZN', start_date, end_date)
    # totp  = pyotp.TOTP("E5V77SMELBEOPE7Y").now()
    # print("Current OTP:", totp)

    # login = rh.login("guptavishu55@gmail.com", "Vpcf1fx!hpvp17", mfa_code=totp)

    # my_stocks = rh.build_holdings()
    # for key,value in my_stocks.items():
    #     print(key,value)





    # gem.get_pubticker("btcusd") # gets ticker information for Bitcoin from Gemini
    # gem.
    # print(rh.get_all_open_crypto_orders()) # gets all cypto orders from Robinhood
    # #print(tda.get_price_history("tsla")) # get price history from TD Ameritrade



