'''
Created on Sep 4, 2018

@author: Ben
'''
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



# spyData= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/NewResearch/TrendTrading/ProbModel/Data/SPY.csv')
#  
# spyData= spyData['Price'].values.tolist()
# spy_dta= pd.Series(spyData, index=pd.date_range('1993-01-01', '2002-11-01', freq='M'))
# mod_spy = sm.tsa.MarkovAutoregression(spy_dta, k_regimes=2, order=4, switching_ar=False)
# res_spy = mod_spy.fit()
#  
# print(res_spy.summary())
# print(res_spy.expected_durations)





djiData= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/NewResearch/TrendTrading/ProbModel/Data/DJI.csv')
djiData= djiData['Price'].values.tolist()
dji_dta= pd.Series(djiData, index=pd.date_range('1985-01-01', '1992-08-01', freq='M'))
mod_dji = sm.tsa.MarkovAutoregression(dji_dta, k_regimes=2, order=4, switching_ar=False)
res_dji = mod_dji.fit()
 
print(res_dji.summary())
print(res_dji.expected_durations)
# 
# 
# 
# 
# 
# iwmData= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/NewResearch/TrendTrading/ProbModel/Data/IWM.csv')
# iwmData= iwmData['Price'].values.tolist()
# iwm_dta= pd.Series(iwmData, index=pd.date_range('2000-05-01', '2018-09-01', freq='D'))
# mod_iwm = sm.tsa.MarkovAutoregression(iwm_dta, k_regimes=2, order=4, switching_ar=False)
# res_iwm = mod_iwm.fit()
# 
# print(res_iwm.summary())
# print(res_iwm.expected_durations)
# 
# 
# 
# 
# 
# ixicData= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/NewResearch/TrendTrading/ProbModel/Data/IXIC.csv')
# ixicData= ixicData['Price'].values.tolist()
# ixic_dta= pd.Series(ixicData, index=pd.date_range('1971-02-01', '1977-01-01', freq='M'))
# mod_ixic = sm.tsa.MarkovAutoregression(ixic_dta, k_regimes=2, order=4, switching_ar=False)
# res_ixic = mod_ixic.fit()
#  
# print(res_ixic.summary())
# print(res_ixic.expected_durations)


