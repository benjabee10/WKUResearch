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
    context.prevstatus=0.5
    context.spy= sid(8554)
    context.sh= sid(32268)

    schedule_function(check)

def check(context, data):

    
    heightspy= data.history(context.spy, 'high', period, '1d')
    peak= heightspy.max()
    trough= heightspy.min()
    current= talib.SMA(heightspy, int(period/45))[-1]
   
    position= context.portfolio.positions[context.spy].amount

    if current > (1+bullthreshold)*trough and not  current < (1-bearthreshold)*peak:
        context.status=1

    elif current < (1-bearthreshold)*peak and not current > (1+bullthreshold)*trough:
        context.status= 0

    elif current < (1-bearthreshold)*peak and current > (1+bullthreshold)*trough:
        if context.bulldays > context.beardays:
            context.status= 0
            
        elif context.bulldays <= context.beardays:
            context.status=1
    
    if context.status != context.prevstatus:
        order_target_percent(context.spy, 0)
        order_target_percent(context.sh, 0)
        
        if context.status==1 and position==0:
            order_target_percent(context.spy, 1)
            
        elif context.status==0:
            order_target_percent(context.sh, 1)
            
    
    
    
    context.days += 1
    context.prevstatus= context.status
    
    if context.status== 1:
        context.bulldays += 1
        
    elif context.status== 0:
        context.beardays += 1

    record(spypeak=context.status, lev=context.account.leverage)