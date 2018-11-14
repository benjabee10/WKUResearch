import numpy as np
import pandas as pd
import talib

lvar= 0.1
mvar= 0.05
svar= 0.025
pct= 0.12
long=0 #(3, 0, -3) (100 day vs 300 day)
medium=0 #(2, 0, -2) (50 day vs 150 day)
short=0 #(1, 0, -1) (10 day vs 30 day)
long1= 100
long2= 300
medium1= 50
medium2= 150
short1= 10
short2= 30
def initialize(context):
    context.stocks= [sid(8347), sid(6653), sid(3149), sid(4151), sid(5061), sid(19675), sid(700), sid(8229)]
    context.spy= sid(8554) 

    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', long2+5, '1d')
    s1= talib.SMA(spydata, short1)[-1]
    s2= talib.SMA(spydata, short2)[-1]
    m1= talib.SMA(spydata, medium1)[-1]
    l1= talib.SMA(spydata, long1)[-1]
    m2= talib.SMA(spydata, medium2)[-1]
    l2= talib.SMA(spydata, long2)[-1]
    
    short= 1*(conditionCheck(s1, s2, svar))
    medium= 2*(conditionCheck(m1, m2, mvar))
    long= 3*(conditionCheck(l1, l2, lvar))
    record(l=long, m=medium, s=short, leverage=context.account.leverage)

def conditionCheck(small, large, var):
    if small > (1+var)*large:
        return 1
    
    elif (1-var)*large < small < (1+var)*large:
        return 0
    
    elif small < (1-var)*large:
        return -1