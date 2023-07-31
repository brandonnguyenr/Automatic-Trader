import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ticker = 'FNGU'
period1 = int(time.mktime(datetime.datetime(2020, 7, 26, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2023, 7, 26, 23, 59).timetuple()))
interval = '1d'  

API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

df = pd.read_csv(API_endpoint)
fast_window = 7 
slow_window = 30  

df['Fast_MA'] = df['Close'].rolling(window=fast_window, min_periods=1).mean()
df['Slow_MA'] = df['Close'].rolling(window=slow_window, min_periods=1).mean()

df.loc[df['Fast_MA'] > df['Slow_MA'], 'Signal'] = 1
df.loc[df['Fast_MA'] < df['Slow_MA'], 'Signal'] = -1

initial_capital = 100000
capital = initial_capital
position = 0  
buy_price = 0

for index, row in df.iterrows():
    if row['Signal'] == 1 and position == 0:  
        position = 1
        buy_price = row['Close']
        shares = capital / buy_price
        capital = 0
    elif row['Signal'] == -1 and position == 1:  
        position = 0
        sell_price = row['Close']
        capital = shares * sell_price
        buy_price = 0

if position == 1:
    position = 0
    sell_price = df['Close'].iloc[-1]
    capital = shares * sell_price
    buy_price = 0

final_profit_loss = capital - initial_capital
percent_profit_margin = (final_profit_loss / initial_capital) * 100

print(f"Final Capital: ${capital:.2f}")
print(f"Profit/Loss: ${final_profit_loss:.2f}")
print(f"Percent Profit Margin: {percent_profit_margin:.2f}%")

xpoints = np.array(df['Date'])
ypoints = np.array(df['Close'])

plt.figure(figsize=(12, 6))
plt.plot(xpoints, ypoints, label='Closing Prices', color='blue')

plt.plot(xpoints, df['Fast_MA'], label=f'{fast_window}-day Fast MA', color='orange')
plt.plot(xpoints, df['Slow_MA'], label=f'{slow_window}-day Slow MA', color='red')

plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Moving Crossover Trading Strategy')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()