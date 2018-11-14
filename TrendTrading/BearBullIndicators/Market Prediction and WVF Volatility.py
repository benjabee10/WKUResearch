import numpy as np
import pandas as pd
import talib

bearthreshold= 0.08
bullthreshold=0.13
period= 90
short=30 
med= 90
long= 180


def initialize(context):
    
    context.status=0.5
    context.days= 0
    context.bulldays= 0
    context.beardays= 0
    context.vxx= sid(38054)
    context.spy= sid(8554)

    schedule_function(check)

def check(context, data):

    
    heightspy= data.history(context.spy, 'high', period, '1d')
    peak= heightspy.max()
    trough= heightspy.min()
    mean= talib.SMA(heightspy, period)[-1]
    current= talib.SMA(heightspy, int(period/45))[-1]
   
    spydata= data.history(context.spy, 'price', long+5, '1d')
    sd= talib.SMA(spydata, short)[-1]
    md= talib.SMA(spydata, med)[-1]
    ld= talib.SMA(spydata, long)[-1]
    
    n = 28
    vxx_prices = data.history(context.vxx, "price", n + 2, "1d")[:-1]
    vxx_lows = data.history(context.vxx, "low", n + 2, "1d")[:-1]
    vxx_highest = vxx_prices.rolling(window = n, center=False).max()    

    WVF = ((vxx_highest - vxx_lows)/(vxx_highest)) * 500

    
    
    shortp= conditionCheck(sd, md, 0.035)
    longp= 2*(conditionCheck(md, ld, 0.035))

    if current > (1+bullthreshold)*trough and not  current < (1-bearthreshold)*peak:
        context.status=1

    elif current < (1-bearthreshold)*peak and not current > (1+bullthreshold)*trough:
        context.status= 0

    elif current < (1-bearthreshold)*peak and current > (1+bullthreshold)*trough:
        if context.bulldays > context.beardays:
            context.status= 0
            
        elif context.bulldays <= context.beardays:
            context.status=1
    
    
    
    
    context.days += 1
    
    if context.status== 1:
        context.bulldays += 1
        
    elif context.status== 0:
        context.beardays += 1

    #record(wvf_vxx = WVF[-1]/100, volbarrier=1.3)
    #record(shortterm= shortp, longterm=longp)
    record(spypeak=context.status)
    
    
def conditionCheck(small, large, var):
    if small > (1+var)*large:
        return 1
    
    elif (1-var)*large < small < (1+var)*large:
        return 0
    
    elif small < (1-var)*large:
        return -1