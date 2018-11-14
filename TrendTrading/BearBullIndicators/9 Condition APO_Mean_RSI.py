import numpy as np
import pandas as pd
import talib

long= 150
med= 50
short= 15
rate=1
#context.market (shortperiod, longperiod):
#Market Values= 0-negative, 1-no trend, 2-positive 

def initialize(context):
    context.secs = [sid(19662),  # XLY Consumer Discrectionary SPDR Fund   
                       sid(19656),  # XLF Financial SPDR Fund  
                       sid(19658),  # XLK Technology SPDR Fund  
                       sid(19655),  # XLE Energy SPDR Fund  
                       sid(19661),  # XLV Health Care SPRD Fund  
                       sid(19657),  # XLI Industrial SPDR Fund  
                       sid(19659),  # XLP Consumer Staples SPDR Fund   
                       sid(19654),  # XLB Materials SPDR Fund  
                       sid(19660)] # XLU Utilities SPRD Fund
    context.spy= sid(8554)
    context.spyetf= sid(32270)
    context.gold= sid(26807)
    context.markettrack= -1
    context.market= -1
    context.longsells= []
    context.shortsells= []
    context.successes= 1
    context.failures= 1

    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', long+5, '1d')
    sd= talib.SMA(spydata, short)[-1]
    md= talib.SMA(spydata, med)[-1]
    ld= talib.SMA(spydata, long)[-1]
    
    shortp= conditionCheck(sd, md, 0.035)
    longp= 2*(conditionCheck(md, ld, 0.035))
    
    checkstatus(context, data)
    
    if shortp==0 and longp==2:
        context.market=12
        if context.market != context.markettrack:
            clearassets(context, data)
            order_target_percent(context.spy, 1)
                        
    elif shortp==0 and longp==0:
        context.market1=11
        if context.market != context.markettrack: 
            clearassets(context, data)
            order_target_percent(context.spy, 1)
            
    elif shortp==0 and longp==-2:
        context.market=10
        if context.market != context.markettrack:  
            clearassets(context, data)
            adxtrade(context, data, 0.5)
            
    elif shortp==1 and longp==2:
        context.market=22
        if context.market != context.markettrack:  
            clearassets(context, data)
            order_target_percent(context.spy, 0.2)
            order_target_percent(context.spyetf, 0.5)
            
    elif shortp==1 and longp==0:
        context.market=21
        if context.market != context.markettrack:  
            clearassets(context, data)
            order_target_percent(context.spy, 0.75)
            
    elif shortp==1 and longp==-2:
        context.market=20
        if context.market != context.markettrack:   
            clearassets(context, data)
            adxtrade(context, data, 0.5)
    
    elif shortp==-1 and longp==2:
        context.market=2
        if context.market != context.markettrack:      
            clearassets(context, data)

    elif shortp==-1 and longp==0:
        context.market=1
        if context.market != context.markettrack:          
            clearassets(context, data)
            adxtrade(context, data, 0.5)
    
    elif shortp==-1 and longp==-2:
        context.market=0
        if context.market != context.markettrack:
            clearassets(context, data)
            order_target_percent(context.spy, -0.5)
            
            order_target_percent(context.gold, 0.5)
            
            
    del context.longsells[:]
    del context.shortsells[:]
    context.markettrack= context.market
    
      
        
    #record(shortperiod=shortp, longperiod=longp, leverage=context.account.leverage)
    record(rate=(context.successes/(context.successes+context.failures)))
    #record(successes= context.successes, fails=context.failures)

def conditionCheck(small, large, var):
    if small > (1+var)*large:
        return 1
    
    elif (1-var)*large < small < (1+var)*large:
        return 0
    
    elif small < (1-var)*large:
        return -1

    
def clearassets(context, data):
    for asset in context.portfolio.positions:
        position = context.portfolio.positions[asset].amount 
        if position <0:
            context.longsells.append(asset)
        elif position >0:
            context.shortsells.append(asset)
            
        order_target_percent(asset, 0)
        
def checkstatus(context, data):
    for asset in context.portfolio.positions:
        position = context.portfolio.positions[asset].amount 
        if position < 0:
            yesterday = data.history(asset, 'price', 2, '1d').iloc[0]
            now= data.current(asset, 'price')
            if now < yesterday:
                context.successes += 1
                
            elif yesterday <= now:
                context.failures += 1
                
        elif position > 0:
            yesterday = data.history(asset, 'price', 2, '1d').iloc[0]
            now= data.current(asset, 'price')
            if now <= yesterday:
                context.failures += 1
                
            elif yesterday < now:
                context.successes += 1
                
    for asset in context.longsells:

        yesterday = data.history(asset, 'price', 2, '1d').iloc[0]
        now= data.current(asset, 'price')
        if now < yesterday:
            context.successes += 1

        elif yesterday <= now:
            context.failures += 1
    
    for asset in context.shortsells:

        yesterday = data.history(asset, 'price', 2, '1d').iloc[0]
        now= data.current(asset, 'price')
        if now > yesterday:
            context.successes += 1

        elif yesterday >= now:
            context.failures += 1      
                       
        
def rsitrade(context, data, alloc):
    pct= alloc/9.0
    low=30
    high=70
    for stock in context.secs:
        prices = data.history(stock, 'price', 15, '1d')
        rsi14= talib.RSI(prices, timeperiod=14)[-1]
        position = context.portfolio.positions[stock].amount            
        if rsi14 > high and position > 0:
            order_target_percent(stock, 0)
        
        elif rsi14 < low and position == 0:
            order_target_percent(stock, pct)
    
def adxtrade(context, data, alloc):
    pct= alloc/9.0

    for stock in context.secs:
        highs = data.history(stock, 'high', 30, '1d')
        lows = data.history(stock, 'low', 30, '1d')
        prices = data.history(stock, 'price', 30, '1d')
        
        adx = talib.ADX(highs, lows, prices, timeperiod=14)[-1]
        mdi= talib.MINUS_DI(highs, lows, prices, timeperiod=14)[-1]
        pdi= talib.PLUS_DI(highs, lows, prices, timeperiod=14)[-1]    
        
        position = context.portfolio.positions[stock].amount
            
        if (adx >20) and (pdi > mdi) and position == 0:
            order_target_percent(stock, pct)

        elif (adx >25) and (pdi < mdi) and position > 0:
            order_target_percent(stock, 0)
            
def meanrevert(context, data, alloc):
    pct= alloc/9.0

    for stock in context.secs:
        prices= data.history(stock, 'price', 10, '1d')
        currentprice= data.current(stock, 'price')
        stddev= prices.std()

        position = context.portfolio.positions[stock].amount
        if stddev > 0:
            zscore = (currentprice - prices)/stddev
        else:
            zscore=0
            
        if zscore >= 1 and position==0:
            order_target_percent(stock, -pct)

        elif zscore <= -1 and position==0:
            order_target_percent(stock, pct)
        
        elif -1 < zscore < 1 and position > 0:
            order_target_percent(stock, 0)