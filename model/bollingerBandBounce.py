from Backtest import BacktestStrategy
from Display import DisplayAdapter as display

class BollingerBandBounce(BacktestStrategy):
    def __init__(self,stock,date1,date2,window):
        # Class for Bollinger Band Bounce serves as an adaptee for the Display class.

        # Args:
        #     stock (DownloadData): selected ETF using the DownloadData object
        #     date1 (str): first date range
        #     date2 (str): second date range
        #     window (str): window date range

        super().__init__(stock,date1,date2)
        self.window = window

    def calculations(self):
        #Performs backtesting calculations
        self.df['MA'] = self.df['Close'].rolling(window=self.window, min_periods=1).mean()
        self.df['std'] = self.df['Close'].rolling(window=self.window, min_periods=1).std()
        self.df['Upper'] = self.df['MA'] + 2 * self.df['std']
        self.df['Lower'] = self.df['MA'] - 2 * self.df['std']
        return
    
    
    def displaySignals(self):
        # displays: Buy/Sell signals, capital gains/loss, percentage gained/loss
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
                shares = self.capital / buy_price
                self.capital = 0
                self.df.loc[index, 'Buy'] = True
                print(f"Buy: {buy_date} | Price: ${buy_price:.2f}")
            elif row['Close'] > row['Upper'] and position == 1:
                position = 0
                sell_price = row['Close']
                sell_date = row['Date']
                self.capital = shares * sell_price
                buy_price = 0
                self.df.loc[index, 'Sell'] = True
                print(f"Sell: {sell_date} | Price: ${sell_price:.2f}")

        if position == 1:
            position = 0
            sell_price = self.df['Close'].iloc[-1]
            self.capital = shares * sell_price
            buy_price = 0
            self.df.loc[self.df.index[-1], 'Sell'] = True
            print(f"Sell: {self.df['Date'].iloc[-1]} | Price: ${sell_price:.2f}")

        self.finalProfitLoss = self.capital - self.initialCapital
        self.profitMarginPercentage = (self.finalProfitLoss / self.initialCapital) * 100

        print(f"\nFinal Capital: ${self.capital:.2f}")
        print(f"Profit/Loss: ${self.finalProfitLoss:.2f}")
        print(f"Percent Profit Margin: {self.profitMarginPercentage:.2f}%\n")
    
    def testStrategy(self):
        self.calculations()
        self.displaySignals()
        d = display(self.stock)
        d.generateBollingerBBGraph(self.getData(),window=self.window)
        return