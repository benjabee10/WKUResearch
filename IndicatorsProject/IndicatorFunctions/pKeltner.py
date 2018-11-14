#potential tweaks: factor (2.25?), range (20?), moving average (EMA?)
import talib
import numpy as np
import pandas as pd

percent= 0.0028
def initialize(context):
    context.stocks1= symbols('AAPL', 'ABT', 'ACN', 'ADBE', 'AES', 'AAP', 'AET', 'AFL', 'AMG', 'A',  'ARE', 'APD', 'AKAM', 'AGN', 'ALXN', 'ADS', 'ALL', 'MO', 'AMZN', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'APA', 'AIV', 'AMAT', 'ADM', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVB', 'AVY', 'BLL', 'BAC', 'BK', 'BAX', 'BBT', 'BDX', 'BBBY',  'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'CHRW', 'CA', 'COG',  'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT',  'CELG',  'CTL', 'CERN', 'CHK', 'CVX', 'CB', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CMS', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'XRAY', 'DVN', 'DO', 'DLTR', 'D', 'DOV', 'DTE',  'DUK', 'DNB', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW',  'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQR', 'ESS', 'EL', 'EXC', 'EXPD', 'ESRX', 'XOM', 'FFIV')   
    context.stocks2= symbols('FAST', 'FDX', 'FITB', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS',  'GPC', 'GILD', 'GS', 'GT',  'GWW', 'HAL', 'HRS', 'HIG', 'HAS',  'HCP', 'HCN', 'HP',  'HD', 'HON', 'HRL', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM',  'KLAC', 'KSS', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LUK', 'LLY', 'LNC', 'LMT', 'L', 'MRO', 'MAR', 'MMC', 'MLM', 'MAS', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET','MCHP', 'MU', 'MSFT', 'MHK', 'MON', 'MCO', 'MS',  'MSI', 'MUR', 'MYL', 'NTAP')    
    context.stocks3= symbols('NWL', 'NFX', 'NEM',  'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PNW', 'PXD', 'PBI', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH',  'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'REGN', 'RSG', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'R', 'SCG', 'SLB', 'SEE', 'SRE', 'SHW', 'SPG',  'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SWK', 'SBUX', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'THC', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TSN', 'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRTX', 'VNO', 'VMC', 'WMT', 'DIS', 'WM', 'WAT', 'WFC', 'WDC', 'WY', 'WHR', 'WMB', 'WEC', 'XEL', 'XRX', 'XLNX', 'XL', 'YUM', 'ZION')
    context.kbrange= 10
    context.factor= 2
    set_benchmark(symbol('SPY'))
    schedule_function(func=trade)

def trade(context, data):
    for stock in context.stocks1:
        if data.can_trade(stock) and not data.is_stale(stock):        
            price = data.current(stock, 'price')    
            position = context.portfolio.positions[stock].amount
            
            highs= data.history(stock, 'high', context.kbrange, '1d')
            lows= data.history(stock, 'low', context.kbrange, '1d')
            prices = data.history(stock, 'price', context.kbrange, '1d')
            try:
                priceset= (highs+lows+prices)/3
                middle= talib.SMA(priceset, timeperiod=context.kbrange)
                shift= context.factor * talib.SMA(highs-lows, timeperiod=context.kbrange)
            except:
                context.stocks1.remove(stock)
                log.info(stock)
                continue
            
            middleval= middle[-1]
            upperval= middleval+ shift[-1]
            lowerval= middleval- shift[-1]
            
            if price <= lowerval and position <= 0:
                order_target_percent(stock, percent)        
            
            elif price >= upperval and position >= 0:
                order_target_percent(stock, 0)

    for stock in context.stocks2:
        if data.can_trade(stock) and not data.is_stale(stock):        
            price = data.current(stock, 'price')    
            position = context.portfolio.positions[stock].amount
            
            highs= data.history(stock, 'high', context.kbrange, '1d')
            lows= data.history(stock, 'low', context.kbrange, '1d')
            prices = data.history(stock, 'price', context.kbrange, '1d')
            try:
                priceset= (highs+lows+prices)/3
                middle= talib.SMA(priceset, timeperiod=context.kbrange)
                shift= context.factor * talib.SMA(highs-lows, timeperiod=context.kbrange)
            except:
                context.stocks2.remove(stock)
                log.info(stock)
                continue
            
            middleval= middle[-1]
            upperval= middleval+ shift[-1]
            lowerval= middleval- shift[-1]
            
            if price <= lowerval and position <= 0:
                order_target_percent(stock, percent)        
            
            elif price >= upperval and position >= 0:
                order_target_percent(stock, 0)

    for stock in context.stocks3:
        if data.can_trade(stock) and not data.is_stale(stock):        
            price = data.current(stock, 'price')    
            position = context.portfolio.positions[stock].amount
            
            highs= data.history(stock, 'high', context.kbrange, '1d')
            lows= data.history(stock, 'low', context.kbrange, '1d')
            prices = data.history(stock, 'price', context.kbrange, '1d')
            try:
                priceset= (highs+lows+prices)/3
                middle= talib.SMA(priceset, timeperiod=context.kbrange)
                shift= context.factor * talib.SMA(highs-lows, timeperiod=context.kbrange)
            except:
                context.stocks3.remove(stock)
                log.info(stock)
                continue
            
            middleval= middle[-1]
            upperval= middleval+ shift[-1]
            lowerval= middleval- shift[-1]
            
            if price <= lowerval and position <= 0:
                order_target_percent(stock, percent)        
            
            elif price >= upperval and position >= 0:
                order_target_percent(stock, 0)
    
    record(leverage=context.account.leverage)