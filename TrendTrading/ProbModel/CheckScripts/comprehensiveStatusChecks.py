'''
This file is designed to determine how often the market index is in a relative bear or bull market state.
This file runs through every daily price of the S&P 500 Index and uses the following steps:
1- Look back over past 180 days
2- Set two thresholds- one that is slightly below the max of last 180 day prices, and one
    that is slightly above the min of last 180 day prices
3- For each of these 180 days, add to the following counts based on that day's prices relative to the thresholds:
    stat0- price is under bottom threshold (bear state)
    stat1- price is between thresholds after coming from below bottom threshold (moderate bull state)
    stat2- price is above top threshold (bull state) 
    statN1- price is between thresholds after coming from above top threshold (moderate bear state)

Then, in the end, the file plots the price, along with the associated thresholds, and prints the amount of times every price 
was in each respective status, along with the percentage of the total share that status accounted for.


'''









import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot

data= pd.read_csv("C:/Users/Ben/iCloudDrive/Workspace/XiaResearch/TrendTrading/ProbModel/Data/SPY19872017.csv")

prices= data['Price']


uppers= []
lowers= []
stat1=0
stat2=0
statN1=0
stat0=0
limit= 180
prevStat=1
for i in range(0, len(prices)-limit):
    
    if i < limit:
        uppers.append(prices[i])
        lowers.append(prices[i])
        
    
    else:
        upper=(np.max(prices[(i-limit+1):i]))*0.95
        lower=(np.min(prices[(i-limit+1):i]))*1.05
        current= prices[i]
        uppers.append(upper)
        lowers.append(lower)  
        
        for j in range(0, limit):
            
        
            if prices[i+j] > upper:
                stat2 += 1
                prevStat=2

            elif prices[i+j] < lower:
                stat0 += 1
                prevStat=0

            elif lower <= prices[i+j] <= upper:
                if prevStat==0 or prevStat==1:
                    stat1 += 1
                    prevStat=1

                elif prevStat==2 or prevStat==-1:
                    statN1 += 1
                    prevStat=-1
                
        
val= len(prices)-limit
totalChecks= stat0+stat1+statN1+stat2
prices= prices[0:val]
                
print('Instances where t was in 0 status:',stat0, "   ", 100*(stat0/totalChecks), "%")
print('Instances where t was in 1 status:',stat1, "   ", 100*(stat1/totalChecks), "%")
print('Instances where t was in 2 status:',stat2, "   ", 100*(stat2/totalChecks), "%")
print('Instances where t was in -1 status:',statN1, "   ", 100*(statN1/totalChecks), "%")
print(totalChecks)

pyplot.plot(prices.index, prices.values, label="prices")
pyplot.plot(prices.index, uppers, label="upper")
pyplot.plot(prices.index, lowers, label="lower")
pyplot.legend(loc="best")
pyplot.show()