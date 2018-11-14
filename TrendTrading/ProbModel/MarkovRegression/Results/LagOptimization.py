import pandas as pd 
import numpy as np 
import statsmodels as sm 
import statistics
import matplotlib.pyplot as plt


np.set_printoptions(suppress=True, formatter={'float_kind':'{:16.3f}'.format}, linewidth=130)

actualData= pd.read_csv('C:/Users/bnj07283/iCloudDrive/Workspace/XiaResearch/TrendTrading/ProbModel/Data/SPY.csv')
actualData = actualData['Price'].values.tolist()

expecteds= [actualData[0], actualData[1], actualData[2]]
ratios= []

for i in range(3, len(actualData)):
	#current period
	lagTest0= actualData[i]
	param0=0.5
	#previous period
	lagTest1= actualData[i-1]
	param1= 0.3
	#two periods ago
	lagTest2= actualData[i-2]
	param2=0.15
	#three periods ago
	lagTest3= actualData[i-3]
	param3= 0.05

	expectedValue= lagTest0*param0+lagTest1*param1+lagTest2*param2+lagTest3*param3
	expecteds.append(expectedValue)

for i in range(0, len(actualData)):
	ratio= (actualData[i]/expecteds[i])
	ratios.append(ratio)

avgRatio= statistics.mean(ratios)
	
print("\n", "Current Period Lag:", param0)
print("\n", "1 Period Ago Lag:", param1)
print("\n", "2 Periods Ago Lag:", param2)
print("\n", "3 Periods Ago Lag:", param3)

print("\n", "Average Ratio between Predicted Value and Actual Value using Current Lags:", avgRatio)

print("\n","Correlation between Actual Data and Predictions", np.corrcoef(actualData, expecteds)[1, 0], "\n")


x = range(120)
y = range(120)
fig = plt.figure()
ax1 = fig.add_subplot(111)

plt.plot(actualData, label="Data")
plt.plot(expecteds, label="ModelResults")
plt.plot(ratios, label="Ratios")
plt.legend(loc="best")
plt.show()
