from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import CustomFactor
from quantopian.pipeline.data.quandl import cboe_vix
from quantopian.pipeline.data.quandl import cboe_vxv

import numpy as np
import pandas as pd


# def rename_col(df):
#   df = df.rename(columns={'Close': 'price','Trade Date': 'Date'})
#  df = df.fillna(method='ffill')
# df = df[['price', 'Settle','sid']]
# Shifting data by TWO dayS TO SIMULATE Q LIVE TRADING PERFORMANCE
# return df.shift(0)


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # securities we are investing in

    context.XIV = symbol('XIV')
    context.VXX = symbol('VXX')
    context.LQD = symbol('LQD')  # Alternative asset when we are waiting for XIV or VXX (HYG is an alternative to lower dd by a little bit, SPY higher beta and returns)
    context.GLD = symbol('GLD')  # Safe Haven when the market is "crazy" - Gold

    my_pipe = Pipeline()
    attach_pipeline(my_pipe, 'my_pipeline')
    # my_pipe.add(GetVIX(inputs=[cboe_vix.vix_open]), 'VixOpen')
    my_pipe.add(GetVIX(inputs=[cboe_vix.vix_close]), 'VixClose')
    # my_pipe.add(GetVIX(inputs=[cboe_vix.vix_high]), 'VixHigh')
    my_pipe.add(GetVIX(inputs=[cboe_vxv.close]), 'VxvClose')

    # Front month VIX futures data
    # fetch_csv('http://www.quandl.com/api/v1/datasets/CHRIS/CBOE_VX1.csv',
    #   date_column='Trade Date',
    #  date_format='%Y-%m-%d',
    # symbol='v1',
    # post_func=rename_col)
    # Second month VIX futures data
    # fetch_csv('http://www.quandl.com/api/v1/datasets/CHRIS/CBOE_VX2.csv',
    #   date_column='Trade Date',
    #  date_format='%Y-%m-%d',
    # symbol='v2',
    # post_func=rename_col)



    # Rebalance every day, 1 minute after market open.
    schedule_function(my_rebalance, date_rules.every_day(), time_rules.market_open(minutes=1))


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.output = pipeline_output('my_pipeline')
    # context.vix = context.output["VixOpen"].iloc[0]
    context.vix = context.output["VixClose"].iloc[0]
    # context.vix = context.output["VixHigh"].iloc[0]
    context.vxv = context.output["VxvClose"].iloc[0]

    print(context.vix, 'vix')
    print(context.vxv, "vxv")


class GetVIX(CustomFactor):
    window_length = 1

    def compute(self, today, assets, out, vix):
        out[:] = vix[-1]


def my_rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """
    # last_ratio = data.current('v1','Settle')/data.current('v2','Settle')
    last_ratio = context.vix / context.vxv
    threshold_bot = 0.9
    threshold_top = 0.95
    vix_top = 21
    vix_bot = 12.5
    # print('vx1', data.current('v1','Settle'))

    if data.can_trade(context.VXX) and data.can_trade(context.XIV):

        # VIX is very high and ratio tells us things are turning bad, we go in safe haven
        if context.vix >= vix_top and last_ratio >= threshold_top:
            order_target_percent(context.VXX, 0)
            order_target_percent(context.XIV, 0)
            order_target_percent(context.LQD, 0)
            order_target_percent(context.GLD, 1)


        # vix is very low and we are not in contango, we suppose vix will raise
        elif context.vix <= vix_bot and last_ratio > threshold_bot:
            order_target_percent(context.VXX, 1)
            order_target_percent(context.XIV, 0)
            order_target_percent(context.LQD, 0)
            order_target_percent(context.GLD, 0)

        # vix is high and we are not in a situation in which the things are turning bad
        elif context.vix >= vix_top and last_ratio < threshold_top:
            order_target_percent(context.VXX, 0)
            order_target_percent(context.XIV, 1)
            order_target_percent(context.LQD, 0)
            order_target_percent(context.GLD, 0)

        # vix is in his standard range and we are in contango
        elif context.vix > vix_bot and context.vix < vix_top and last_ratio < threshold_bot:
            order_target_percent(context.VXX, 0)
            order_target_percent(context.XIV,
                                 1)  # a valuable option is to leverage here in order to achieve higher returns
            order_target_percent(context.LQD, 0)
            order_target_percent(context.GLD, 0)

        # vix is in his standard range but we are not in contango, we wait switching to bonds
        elif context.vix > vix_bot and context.vix < vix_top and last_ratio > threshold_bot and last_ratio < threshold_top:
            order_target_percent(context.VXX, 0)
            order_target_percent(context.XIV, 0)
            order_target_percent(context.LQD, 1)
            order_target_percent(context.GLD, 0)


            # when there is conflict between signals we switch to bonds
        elif context.vix < vix_bot and last_ratio < threshold_bot:
            order_target_percent(context.VXX, 0)
            order_target_percent(context.XIV, 0)
            order_target_percent(context.LQD, 1)
            order_target_percent(context.GLD, 0)

    record(XIV_exposure=context.portfolio.positions[symbol('XIV')].amount)
    record(VXX_exposure=context.portfolio.positions[symbol('VXX')].amount)
    record(LQD_exposure=context.portfolio.positions[symbol('LQD')].amount)
    # record(VIX=context.vix)
    record(ratio=last_ratio)
    record(leverage=context.account.leverage)