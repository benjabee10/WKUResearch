import numpy as np
import pandas as pd
import talib

low=0.95
high=1.05
pct= 0.12
def initialize(context):
    context.stocks= [sid(8347), sid(6653), sid(3149), sid(4151), sid(5061), sid(19675), sid(700), sid(8229)]
    context.spy= sid(8554)

    context.market= 0
    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', 210, '1d')
    spy50= talib.SMA(spydata, 50)[-1]
    spy200= talib.SMA(spydata, 200)[-1]
    
    if spy50 > high*spy200:
        context.market= 1

    elif low*spy200 < spy50 < high*spy200:
        context.market= 0

    elif spy50 < low*spy200:
        context.market= -1

    spyposition = context.portfolio.positions[context.spy].amount


    if context.market == 1 and spyposition==0:
        order_target_percent(context.spy, 1)
        clearstocks(context, data)

    elif context.market == 0:
        apotrade(context, data)
        order_target_percent(context.spy, 0)

    elif context.market == -1 and spyposition==0:
        order_target_percent(context.spy, -1)
        clearstocks(context, data)
        
    record(market=context.market, leverage=context.account.leverage)
    
def apotrade(context, data):
    for stock in context.stocks:
        prices = data.history(stock, 'price', 50, '1d')
        apo = talib.APO(prices, fastperiod=12, slowperiod=26, matype=0)[-1]
        position = context.portfolio.positions[stock].amount        
        if apo > 0 and position == 0:
            order_target_percent(stock, pct)

        elif apo < 0 and position > 0:
            order_target_percent(stock, 0)

def clearstocks(context, data):
    for stock in context.stocks:
        order_target_percent(stock, 0)