import numpy as np
import pandas as pd 
import statsmodels.api as sm
import matplotlib.pyplot as pyplot


spyData= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/NewResearch/TrendTrading/ProbModel/Data/SPY.csv')
spyData= spyData['Price'].values.tolist()
spy_dta= pd.Series(spyData, index=pd.date_range('1996-04-09', '2006-02-05', freq='M'))
mod_spy = sm.tsa.MarkovAutoregression(spy_dta, k_regimes=2, order=4, switching_ar=False)
res_spy = mod_spy.fit()

np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)

print(res_spy.summary(), "\n")
# print(res_spy.expected_durations, "\n")
# 
# print(mod_spy.initial_probabilities(mod_spy.start_params), "\n")
# 
# print(mod_spy.predict(mod_spy.start_params), "\n")
# 
# print(mod_spy.regime_transition_matrix(mod_spy.transform_params(mod_spy.start_params)))


mod_spy.initialize_known([0.3, 0.7])

# print(mod_spy.score_obs(mod_spy.start_params))
print(mod_spy.param_names)
print(mod_spy.start_params)
print(mod_spy.start_params.shape)

testParams= np.array([0.300, 0.700, 0.000, 0.704, 11.113, 0.910, 0.027, 0.163, -0.117])
print(testParams)