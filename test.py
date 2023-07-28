import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ticker = 'FNGU'
period1 = int(time.mktime(datetime.datetime(2020, 7, 26, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2023, 7, 26, 23, 59).timetuple()))
interval = '1d' # 1d, 1m

API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

df = pd.read_csv(API_endpoint)
print(df)

temp = df.to_dict()

date = list(temp['Date'])
print(date)
close = np.fromiter(temp['Close'].values(), dtype=float)

xpoints = np.array(date)
ypoints = np.array(close)

plt.plot(xpoints, ypoints)
plt.show()