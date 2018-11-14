'''
Created on Sep 11, 2018

@author: Ben
'''

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sn

# NBER recessions
from pandas_datareader.data import DataReader
from datetime import datetime
usrec = DataReader('USREC', 'fred', start=datetime(1947, 1, 1), end=datetime(2013, 4, 1))

from statsmodels.tsa.regime_switching.tests.test_markov_autoregression import rgnp
dta_hamilton = pd.Series(rgnp, index=pd.date_range('1951-04-01', '1984-10-01', freq='QS'))

print(dta_hamilton)
# Plot the data
dta_hamilton.plot(title='Growth rate of Real GNP', figsize=(12,3))

plt.show()

# Fit the model
mod_hamilton = sm.tsa.MarkovAutoregression(dta_hamilton, k_regimes=2, order=4, switching_ar=False)
res_hamilton = mod_hamilton.fit()

print(res_hamilton.summary())


fig, axes = plt.subplots(2, figsize=(7,7))
ax = axes[0]
ax.plot(res_hamilton.filtered_marginal_probabilities[0])
ax.fill_between(usrec.index, 0, 1, where=usrec['USREC'].values, color='gray', alpha=0.3)
ax.set(xlim=(dta_hamilton.index[4], dta_hamilton.index[-1]), ylim=(0, 1),
       title='Filtered probability of recession')

ax = axes[1]
ax.plot(res_hamilton.smoothed_marginal_probabilities[0])
ax.fill_between(usrec.index, 0, 1, where=usrec['USREC'].values, color='gray', alpha=0.3)
ax.set(xlim=(dta_hamilton.index[4], dta_hamilton.index[-1]), ylim=(0, 1),
       title='Smoothed probability of recession')

plt.show()
fig.tight_layout()

print(res_hamilton.expected_durations)
