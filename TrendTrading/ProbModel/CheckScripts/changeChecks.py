import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot

data= pd.read_csv('C:/Users/Ben/iCloudDrive/EclipseWorkspace/ResearchBase/TrendTrading/ProbModel/SPY19872017.csv', names=['date', 'price'])
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

for i in range(limit, length-limit):
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

