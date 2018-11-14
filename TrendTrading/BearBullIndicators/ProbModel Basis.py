import numpy as np
import pandas as pd
import talib

bearthreshold= 0.06
bullthreshold=0.08
period= 90




def initialize(context):
    
    context.vxx= sid(38054)
    context.status=0.5
    context.days= 0
    context.temp= -5
    context.outStatus=-1
    context.prevOut= -1
    context.spyload= 0
    context.volBarrier= 1.75


    context.spy= sid(8554)


    schedule_function(check)

def check(context, data):
    
    heightspy= data.history(context.spy, 'price', period, '1d')
    peak= heightspy.max()
    trough= heightspy.min()
    current= data.current(context.spy, 'price')
       
    overLow= current >= (1+bullthreshold)*trough
    underHigh= current < (1-bearthreshold)*peak
    
    n = 28
    vxx_prices = data.history(context.vxx, "price", n + 2, "1d")[:-1]
    vxx_lows = data.history(context.vxx, "low", n + 2, "1d")[:-1]
    vxx_highest = vxx_prices.rolling(window = n, center=False).max()    

    WVF = ((vxx_highest - vxx_lows)/(vxx_highest)) * 5
    
    
    if context.days <= 1:
        context.status= initial(context, data)
        context.temp= context.status

    else:
        if WVF[-1] < context.volBarrier:
            if (1+bullthreshold)*trough >(1-bearthreshold)*peak:
                context.outStatus= context.prevOut

            elif context.status==0 and not overLow:
                context.temp= 0

            elif (context.status==1 or context.status==-1) and underHigh and not overLow:
                context.temp= 0

            elif context.status==2 and not underHigh:
                context.temp=2

            elif (context.status==1 or context.status==-1) and not underHigh and overLow:
                context.temp=2

            elif context.status==2 and underHigh and overLow:
                context.temp=-1

            elif context.status==1 and underHigh and overLow:
                context.temp=1

            elif context.status==-1 and underHigh and overLow:
                context.temp=-1

            elif context.status==0 and underHigh and overLow:
                context.temp=1

    

    
    
    if context.temp==0 or context.temp==-1:
        context.outStatus= 0
        
    elif context.temp==1 or context.temp==2:
        context.outStatus= 1
        
    if context.outStatus != context.prevOut:
        if context.outStatus==0:
            order_target_percent(context.spy, 0)
            context.spyload= 0
            
        elif context.outStatus==1:
            order_target_percent(context.spy, 0)
            order_target_percent(context.spy, 1)
            context.spyload=1
    
        
       
    context.days += 1
    context.status= context.temp
    context.prevOut= context.outStatus
    
    #record(bottom=(1+bullthreshold)*trough, top=(1-bearthreshold)*peak, cur=current)
    #record(wvf_vxx = WVF[-1], volbarrier=context.volBarrier)
    record(stat=context.outStatus, spyamt=context.spyload, lev=context.account.leverage)
    record(wvf_vxx = WVF[-1], volbarrier=context.volBarrier)

    
def initial(context, data):
    
    maxChanges= 0
    minChanges= 0
    pricing= data.history(context.spy, 'price', period, '1d')
    initMax= pricing[-period]
    initMin=pricing[-period]
    for i in range(-period, 0):
        if pricing[i] > initMax:
            maxChanges += 1
            initMax=pricing[i]
            
        if pricing[i] < initMin:
            minChanges += 1
            initMin=pricing[i]
            
        if maxChanges ==3 or minChanges==3:
            if maxChanges > minChanges:
                return 1
            
            elif maxChanges < minChanges:
                return 0