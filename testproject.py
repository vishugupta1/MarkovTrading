import ManualStrategy as ms
import datetime as dt
import experiment1 as exp1
import experiment2 as exp2


if __name__ == '__main__':
    # commission - $9.95 
    # impact - .005

    # need to import stock data from online resource: 
    


    
    
    # in sample
    trades=ms.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1),ed =dt.datetime(2009, 1, 1), sv=100000)
    ms.create_charts_MS(symbol="JPM", sd=dt.datetime(2008, 1, 1),ed=dt.datetime(2009, 1, 1), trades=trades, sv=100000, title="ManualStrategy_InSample")

    # # # out of sample
    trades=ms.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1),ed=dt.datetime(2011, 1, 1), sv=100000)
    ms.create_charts_MS(symbol="JPM", sd=dt.datetime(2010, 1, 1),ed=dt.datetime(2011, 1, 1), trades=trades, sv=100000, title="ManualStrategy_OutSample")

    exp1.main()
    # exp2.main()




