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
window = 7  

df['MA'] = df['Close'].rolling(window=window, min_periods=1).mean()
df['std'] = df['Close'].rolling(window=window, min_periods=1).std()
df['Upper'] = df['MA'] + 2 * df['std']
df['Lower'] = df['MA'] - 2 * df['std']

initial_capital = 100000
capital = initial_capital
position = 0  
buy_price = 0

for index, row in df.iterrows():
    if row['Close'] < row['Lower'] and position == 0:  
        position = 1
        buy_price = row['Close']
        shares = capital / buy_price
        capital = 0
    elif row['Close'] > row['Upper'] and position == 1:  
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

plt.plot(xpoints, df['MA'], label=f'{window}-day MA', color='orange')
plt.fill_between(xpoints, df['Upper'], df['MA'], alpha=0.2, color='green', label='Upper Bollinger Band')
plt.fill_between(xpoints, df['MA'], df['Lower'], alpha=0.2, color='red', label='Lower Bollinger Band')

plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Bollinger Band Bounce Trading Strategy')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()