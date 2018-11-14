
# coding: utf-8

# In[29]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot



data= get_pricing("SPY", start_date="2003-1-1", end_date="2018-1-1")

prices= data['price']


uppers= []
lowers= []

upBull=0
upBear=0
downBull=0
downBear=0
bearUp=0
bullDown=0


limit= 180

prevStat=-2
tempStat=-2
length= len(prices)
print(length)

def initial():
    
    maxChanges= 0
    minChanges= 0
    initMax= prices[1]
    initMin=prices[1]
    for i in range(2, limit):
        if prices[i] > initMax:
            maxChanges += 1
            initMax=prices[i]
            
        if prices[i] < initMin:
            minChanges += 1
            initMin=prices[i]
            
        if maxChanges == 3 or minChanges==3:
            if maxChanges > minChanges:
                prevStat=1
                tempStat=1
            
            elif maxChanges < minChanges:
                prevStat=-1
                tempStat=-1


initial()

for i in range(0, length):
    if i < limit:
        uppers.append(prices[i])
        lowers.append(prices[i])
    
    else:
        upper=(np.max(prices[(i-limit+1):i]))*0.95

        lower=(np.min(prices[(i-limit+1):i]))*1.05


        uppers.append(upper)
        lowers.append(lower)  
        if prices[i] > upper:
            tempStat=2
            
        elif prices[i] < lower:
            tempStat=0
            
        elif lower <= prices[i] <= upper:
            if prevStat==0 or prevStat==1:
                tempStat=1
                
            elif prevStat==2 or prevStat==-1:
                tempStat=-1

        
        if prevStat != tempStat:
            if prevStat==1 and tempStat==2:
                upBull +=1

            elif prevStat==-1 and tempStat==2:
                downBull += 1

            elif prevStat==1 and tempStat==0:
                upBear +=1

            elif prevStat==-1 and tempStat==0:
                downBear +=1

            elif prevStat==2 and tempStat==-1:
                bullDown +=1

            elif prevStat==0 and tempStat==1:
                bearUp += 1
            


        prevStat= tempStat


        
                
        
        

print("Number of Changes from 1 to 2:", upBull)
print("Number of Changes from 1 to 0:", upBear)
print("Number of Changes from -1 to 2:", downBull) 
print("Number of Changes from -1 to 0:", downBear)
print("Number of Changes from 0 to 1:", bearUp) 
print("Number of Changes from 2 to -1:", bullDown)    

pyplot.plot(prices.index, prices.values, label="prices")
pyplot.plot(prices.index, uppers, label="upper")
pyplot.plot(prices.index, lowers, label="lower")
pyplot.legend(loc="best")


# In[30]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot
import talib



data= get_pricing("SPY", start_date="2003-1-1", end_date="2018-1-1")

prices= data['price']


uppers= []
lowers= []

upBull=0
upBear=0
downBull=0
downBear=0
bearUp=0
bullDown=0
macdVal=0
macdVals=[]
upper=1
lower=-1


limit= 180

prevStat=1
tempStat=1
length= len(prices)
print(length)


for i in range(0, length):
    
    macd, signal, hist = talib.MACDEXT(prices, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
    macdVal= macd[-i] - signal[-i]
    macdVals.append(macdVal)

    if macdVal >upper:
        tempStat=2

    elif macdVal < lower:
        tempStat=0

    elif lower <= macdVal <= upper:
        if prevStat==0 or prevStat==1:
            tempStat=1

        elif prevStat==2 or prevStat==-1:
            tempStat=-1



    if prevStat != tempStat:
        if prevStat==1 and tempStat==2:
            upBull +=1

        elif prevStat==-1 and tempStat==2:
            downBull += 1

        elif prevStat==1 and tempStat==0:
            upBear +=1

        elif prevStat==-1 and tempStat==0:
            downBear +=1

        elif prevStat==2 and tempStat==-1:
            bullDown +=1

        elif prevStat==0 and tempStat==1:
            bearUp += 1



    prevStat= tempStat


        
                
        
        
print(len(macdVals))
print("Number of Changes from 1 to 2:", upBull)
print("Number of Changes from 1 to 0:", upBear)
print("Number of Changes from -1 to 2:", downBull) 
print("Number of Changes from -1 to 0:", downBear)
print("Number of Changes from 0 to 1:", bearUp) 
print("Number of Changes from 2 to -1:", bullDown)  

pyplot.plot(prices.index, macdVals, label="MACD")
pyplot.legend(loc="best")


# In[32]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot
import talib



data= get_pricing("SPY", start_date="2003-1-1", end_date="2018-1-1")

prices= data['price']


uppers= []
lowers= []

upBull=0
upBear=0
downBull=0
downBear=0
bearUp=0
bullDown=0
rsiVal=0
rsiVals=[]
upper=70
lower=30


limit= 180

prevStat=1
tempStat=1
length= len(prices)
print(length)


for i in range(0, length):
    
    rsiVal= talib.RSI(prices, timeperiod=14)[-i]
    rsiVals.append(rsiVal)

    if rsiVal >upper:
        tempStat=2

    elif rsiVal < lower:
        tempStat=0

    elif lower <= rsiVal <= upper:
        if prevStat==0 or prevStat==1:
            tempStat=1

        elif prevStat==2 or prevStat==-1:
            tempStat=-1



    if prevStat != tempStat:
        if prevStat==1 and tempStat==2:
            upBull +=1

        elif prevStat==-1 and tempStat==2:
            downBull += 1

        elif prevStat==1 and tempStat==0:
            upBear +=1

        elif prevStat==-1 and tempStat==0:
            downBear +=1

        elif prevStat==2 and tempStat==-1:
            bullDown +=1

        elif prevStat==0 and tempStat==1:
            bearUp += 1



    prevStat= tempStat


        
                
        
        
print(len(macdVals))
print("Number of Changes from 1 to 2:", upBull)
print("Number of Changes from 1 to 0:", upBear)
print("Number of Changes from -1 to 2:", downBull) 
print("Number of Changes from -1 to 0:", downBear)
print("Number of Changes from 0 to 1:", bearUp) 
print("Number of Changes from 2 to -1:", bullDown)  

pyplot.plot(prices.index, rsiVals, label="prices")
pyplot.legend(loc="best")

