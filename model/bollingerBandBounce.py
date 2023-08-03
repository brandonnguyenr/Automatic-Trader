
class BollingerBandBounce:

    def __init__(self,stock,date1,date2,window):
        self.date1 = date1
        self.date2 = date2
        self.stock = stock
        self.df = self.stock.getCSV()
        self.window = window

    def calculations(self):
        self.df['MA'] = self.df['Close'].rolling(window=self.window, min_periods=1).mean()
        self.df['std'] = self.df['Close'].rolling(window=self.window, min_periods=1).std()

        self.df['Upper'] = self.df['MA'] + 2 * self.df['std']
        self.df['Lower'] = self.df['MA'] - 2 * self.df['std']

        return
    
    def getData(self):
        return self.df
    
    def displaySignals(self):
        initial_capital = 100000
        capital = initial_capital
        position = 0
        buy_price = 0
        buy_date = None
        sell_date = None

        self.df['Buy'] = False
        self.df['Sell'] = False
        
        for index, row in self.df.iterrows():
            if row['Close'] < row['Lower'] and position == 0:
                position = 1
                buy_price = row['Close']
                buy_date = row['Date']
                shares = capital / buy_price
                capital = 0
                self.df.loc[index, 'Buy'] = True
                print(f"Buy: {buy_date} | Price: ${buy_price:.2f}")
            elif row['Close'] > row['Upper'] and position == 1:
                position = 0
                sell_price = row['Close']
                sell_date = row['Date']
                capital = shares * sell_price
                buy_price = 0
                self.df.loc[index, 'Sell'] = True
                print(f"Sell: {sell_date} | Price: ${sell_price:.2f}")

        if position == 1:
            position = 0
            sell_price = self.df['Close'].iloc[-1]
            capital = shares * sell_price
            buy_price = 0
            self.df.loc[self.df.index[-1], 'Sell'] = True
            print(f"Sell: {self.df['Date'].iloc[-1]} | Price: ${sell_price:.2f}")

        final_profit_loss = capital - initial_capital
        percent_profit_margin = (final_profit_loss / initial_capital) * 100

        print(f"\nFinal Capital: ${capital:.2f}")
        print(f"Profit/Loss: ${final_profit_loss:.2f}")
        print(f"Percent Profit Margin: {percent_profit_margin:.2f}%\n")
    