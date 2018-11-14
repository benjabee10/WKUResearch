import numpy as np
import pandas as pd
import talib

bearthreshold= 0.15
bullthreshold=0.2
period= 90
status=0


def initialize(context):
    
    context.spy= sid(8554)

    schedule_function(check)

def check(context, data):
    spydata= data.history(context.spy, 'price', period+5, '1d')
    peak= data.history(context.spy, 'high', period, '1d')
    trough= data.history(context.spy, 'low', period, '1d')
    current= data.current(context.spy, 'price')

    if current > (1+bullthreshold)* trough:
        status=1

    elif current < (1-bearthreshold)* peak:
        status= -1

    else:
        status= 0


    record(stat=status)


