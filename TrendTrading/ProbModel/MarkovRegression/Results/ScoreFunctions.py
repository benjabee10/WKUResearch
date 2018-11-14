
import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd 
import statsmodels.api as sm
import matplotlib.pyplot as plt

spyData = pd.read_csv('C:/Users/Ben/iCloudDrive/Workspace/XiaResearch/TrendTrading/ProbModel/Data/SPY.csv')
spyData = spyData['Price'].values.tolist()
spy_dta = pd.Series(spyData, index=pd.date_range('1996-04-09', '2006-02-05', freq='M'))
mod_spy = sm.tsa.MarkovAutoregression(spy_dta, k_regimes=2, order=4, switching_ar=False)
res_spy= mod_spy.fit()

np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)




predictions= mod_spy.predict(mod_spy.start_params)

predictions= np.concatenate([[spyData[0], spyData[1], spyData[2], spyData[3]], predictions])
predictions.flatten()


print("\n","Lagged Correlation between actual data and predictions", np.corrcoef(spyData[:len(predictions)], predictions)[1, 0], "\n")

print("\n", "P-Value of Lagged Cointegration between actual data and predictions",
       ts.coint(spyData[:len(predictions)], predictions)[1], "\n")
print("\n", "99%, 95%, and 90% Confidence Interval Critical Values", ts.coint(spyData[:len(predictions)], predictions)[2], "\n")


x = range(120)
y = range(120)
fig = plt.figure()
ax1 = fig.add_subplot(111)

plt.plot(spyData, label="Data")
plt.plot(predictions, label="Predictions")
plt.legend(loc="best")
plt.show()


