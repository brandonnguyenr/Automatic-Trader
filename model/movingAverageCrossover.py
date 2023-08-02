import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import DownloadData as dd

def mva():
    etf = input("Enter ETF (FNGD/FNGU): ")
    date1 = input("Enter start date (MMDDYYYY): ")
    date2 = input("Enter end date (MMDDYYYY): ")
    stock = dd.DownloadData(etf,date1,date2)
    ticker = etf
    period1 = int(time.mktime(datetime.datetime(int(date1[-4:]), int(date1[:2]), int(date1[2:4]), 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(int(date2[-4:]), int(date2[:2]), int(date2[2:4]), 23, 59).timetuple()))
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
    buy_date = None
    sell_date = None

    df['Buy'] = False
    df['Sell'] = False

    for index, row in df.iterrows():
        if row['Signal'] == 1 and position == 0:  
            position = 1
            buy_price = row['Close']
            buy_date = row['Date']
            shares = capital / buy_price
            capital = 0
            df.loc[index, 'Buy'] = True
            print(f"Buy: {buy_date} | Price: ${buy_price:.2f}")
        elif row['Signal'] == -1 and position == 1:  
            position = 0
            sell_price = row['Close']
            sell_date = row['Date']
            capital = shares * sell_price
            buy_price = 0
            df.loc[index, 'Sell'] = True
            print(f"Sell: {sell_date} | Price: ${sell_price:.2f}")

    if position == 1:
        position = 0
        sell_price = df['Close'].iloc[-1]
        capital = shares * sell_price
        buy_price = 0
        df.loc[df.index[-1], 'Sell'] = True
        print(f"Sell: {df['Date'].iloc[-1]} | Price: ${sell_price:.2f}")

    final_profit_loss = capital - initial_capital
    percent_profit_margin = (final_profit_loss / initial_capital) * 100

    print(f"\nFinal Capital: ${capital:.2f}")
    print(f"Profit/Loss: ${final_profit_loss:.2f}")
    print(f"Percent Profit Margin: {percent_profit_margin:.2f}%\n")

    xpoints = stock.getDate()
    ypoints = np.array(df['Close'])

    plt.figure(figsize=(12, 6))
    plt.plot(xpoints, ypoints, label='Closing Prices', color='blue')

    plt.plot(xpoints, df['Fast_MA'], label=f'{fast_window}-day Fast MA', color='orange')
    plt.plot(xpoints, df['Slow_MA'], label=f'{slow_window}-day Slow MA', color='red')

    # Add buy/sell points to the graph
    plt.scatter(df[df['Buy'] == True]['Date'], df[df['Buy'] == True]['Close'], marker='^', color='g', label='Buy', lw=0)
    plt.scatter(df[df['Sell'] == True]['Date'], df[df['Sell'] == True]['Close'], marker='v', color='r', label='Sell', lw=0)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('Moving Crossover Trading Strategy')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()