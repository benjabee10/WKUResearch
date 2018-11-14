import numpy as np
import pandas as pd
import talib

upperBound= 0.14
lowerBound=0.15
period= 180




def initialize(context):
       
    context.status=0.5
    context.days= 0
    context.daySinceChange=0


    context.spy= sid(8554)


    schedule_function(check)

def check(context, data):
    
    current= data.current(context.spy, 'price')
    prices= data.history(context.spy, 'price', period, '1d')
    localPeak= prices.max()
    localTrough= prices.min()
    
    if context.daySinceChange > period:
        if context.status==1:
            context.peak=localPeak
            
        elif context.status==0:
            context.trough=localTrough
    
    
    
    if context.days <1:
        context.status= initial(context, data)
        context.trough=localTrough
        context.peak=localPeak
        log.info("day 1")
        context.days += 1
        return
    
    
    if context.status ==1:
        if (1-upperBound)*context.peak > current:
            context.status=0
            context.trough=current
            context.daySinceChange=0
                       
        
    elif context.status ==0:
        if (1+lowerBound)*context.trough < current:
            context.status=1
            context.peak=current
            context.daySinceChange=0
    
    
    
    context.daySinceChange += 1
    context.days += 1
    
    record(stat=context.status)
    
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