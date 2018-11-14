'''
Created on Aug 26, 2018

@author: Ben Davison
'''

import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot
import statsmodels.api as sm
import matplotlib.pyplot as plt
import requests
from io import BytesIO


from statsmodels.tsa.regime_switching.tests.test_markov_autoregression import rgnp
from pandas_datareader.data import DataReader
from datetime import datetime


spyData= pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/XiaResearch/TrendTrading/ProbModel/Data/SPY.csv')
print(spyData)
spyData= spyData['Price'].values.tolist()


spy_dta= pd.Series(spyData, index=pd.date_range('1996-04-09', '2006-02-05', freq='M'))

#print(spy_dta)
#spy_dta.plot(title='SPY Log Returns (By Percentage)', figsize=(12,3))
#plt.show()

mod_spy = sm.tsa.MarkovAutoregression(spy_dta, k_regimes=2, order=4, switching_ar=False)
res_spy = mod_spy.fit()

#plt.show()
print(res_spy.summary())
print(res_spy.expected_durations)


