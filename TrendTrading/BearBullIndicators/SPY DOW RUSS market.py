import numpy as np
import pandas as pd
import talib

low=0.9
high=1.1
pct= 0.1
def initialize(context):
    context.stocks= [sid(8347), sid(6653), sid(3149), sid(4151), sid(5061), sid(19675), sid(700), sid(8229)]
    context.spy= sid(8554)
    context.russ= sid(21519)
    context.dow= sid(2174)
    context.small= 50
    context.large= 200

    context.market= 0
    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', context.large+10, '1d')
    spys= talib.SMA(spydata, context.small)[-1]
    spyl= talib.SMA(spydata, context.large)[-1]
    russdata= data.history(context.russ, 'price', context.large+10, '1d')
    russs= talib.SMA(russdata, context.small)[-1]
    russl= talib.SMA(russdata, context.large)[-1]
    dowdata= data.history(context.dow, 'price', context.large+10, '1d')
    dows= talib.SMA(dowdata, context.small)[-1]
    dowl= talib.SMA(dowdata, context.large)[-1]
    
    
    if spys > high*spyl and russs > high*russl and dows > high*dowl:
        context.market= -1

    elif low*spyl <= spys <= high*spyl or low*russl <= russs <= high*russl or low*dowl <= dows <= high*dowl:
        context.market= 0

    elif spys < low*spyl and russs < low*russl and dows < low*dowl:
        context.market= 1

    spyposition = context.portfolio.positions[context.spy].amount
    russposition = context.portfolio.positions[context.russ].amount
    dowposition = context.portfolio.positions[context.spy].amount

    if context.market == 1 and spyposition==0:
        order_target_percent(context.spy, 0.3)
        order_target_percent(context.russ, 0.3)
        order_target_percent(context.dow, 0.3)
        clearstocks(context, data)

    elif context.market == 0:
        apotrade(context, data)
        order_target_percent(context.spy, 0)
        order_target_percent(context.russ, 0)
        order_target_percent(context.dow, 0)

    elif context.market == -1 and spyposition==0:
        order_target_percent(context.spy, -0.3)
        order_target_percent(context.russ, -0.3)
        order_target_percent(context.dow, -0.3)
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