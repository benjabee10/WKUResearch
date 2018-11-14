import numpy as np
import pandas as pd
import talib

big= 200
small= 50
threshold=0.02
#context.market (shortperiod, longperiod):
#Market Values= 0-negative, 1-no trend, 2-positive 

def initialize(context):
    
    context.spy= sid(8554)

    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', big+5, '1d')
    lAvg= talib.SMA(spydata, small)[-1]
    sAvg= talib.SMA(spydata, big)[-1]
    shortAvgY= talib.SMA(spydata, small)[-2]
    longAvgY= talib.SMA(spydata, big)[-2]
    
    shortp= conditionCheck(sd, md, threshold)
    longp= 2*(conditionCheck(md, ld, threshold))
    
    
    context.markettrack= context.market

def conditionCheck(small, large, smallY, largeY var):
    if small > (1+var)*small and large > (1+var)*large:
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
