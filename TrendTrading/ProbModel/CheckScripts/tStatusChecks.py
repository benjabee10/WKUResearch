import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot

data= pd.read_csv('/Users/bendavison/SPY19872017.csv', names=['date', 'price'])
prices= data['price']



uppers= []
lowers= []
stat1=0
stat2=0
statN1=0
stat0=0
limit= 180
prevStat=1
print(len(prices))
for i in range(0, len(prices)):
    if i < limit:
        uppers.append(prices[i])
        lowers.append(prices[i])
    
    else:
        upper=(np.max(prices[(i-limit+1):i]))*0.95
        lower=(np.min(prices[(i-limit+1):i]))*1.05
        current= prices[i]
        uppers.append(upper)
        lowers.append(lower)  
        if prices[i] > upper:
            stat2 += 1
            prevStat=2
            
        elif prices[i] < lower:
            stat0 += 1
            prevStat=0
            
        elif lower <= prices[i] <= upper:
            if prevStat==0 or prevStat==1:
                stat1 += 1
                prevStat=1
                
            elif prevStat==2 or prevStat==-1:
                statN1 += 1
                prevStat=-1
                
        
        
                
    
print('Instances where t was in 0 status:',stat0)
print('Instances where t was in 1 status:',stat1)
print('Instances where t was in 2 status:',stat2)
print('Instances where t was in -1 status:',statN1)
print(stat0+stat1+statN1+stat2)
pyplot.plot(prices.index, prices.values, label="prices")
pyplot.plot(prices.index, uppers, label="upper")
pyplot.plot(prices.index, lowers, label="lower")
pyplot.legend(loc="best")