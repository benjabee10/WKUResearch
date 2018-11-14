import numpy as np
import pandas as pd 
import matplotlib.pyplot as pyplot 

sym= "SPY"
df_close= pd.DataFrame()
df_temp= pd.read_json('https://api.iextrading.com/1.0/stock/'+sym+'/chart/10y')
df.temp_head(4)