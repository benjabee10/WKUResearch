def initialize(context):
    context.spy= sid(8554)
    schedule_function(my_rebalance, date_rules.month_start(), time_rules.market_open())
 
def my_rebalance(context,data):
    position= context.portfolio.positions[context.spy].amount
    if position == 0:
        order_target_percent(context.spy, 1.0)
        
    record(lev=context.account.leverage)