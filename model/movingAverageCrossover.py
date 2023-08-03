from Backtest import Backtest
import Display as display

class MovingAverageCrossover(Backtest):
    def __init__(self,stock,date1,date2,slow,fast):
        # Class for Moving Average Crossover
        # Args:
        #     stock (str): selected ETF using the DownloadData object
        #     date1 (str): first date range
        #     date2 (str): second date range
        #     slow (str): slow moving average line
        #     fast (str): fast moving average line

        super().__init__(stock,date1,date2)
        self.fast = fast
        self.slow = slow
    
    def calculations(self):
        #Performs calculations and is stored in self.df, does not need to return anything 
        self.df['Fast_MA'] = self.df['Close'].rolling(window=self.fast, min_periods=1).mean()
        self.df['Slow_MA'] = self.df['Close'].rolling(window=self.slow, min_periods=1).mean()
        self.df.loc[self.df['Fast_MA'] > self.df['Slow_MA'], 'Signal'] = 1
        self.df.loc[self.df['Fast_MA'] < self.df['Slow_MA'], 'Signal'] = -1
        return
    
    
    def displaySignals(self):
        #displays: Buy/Sell signals, capital gains/loss, percentage gained/loss
        position = 0  
        buy_price = 0
        buy_date = None
        sell_date = None

        self.df['Buy'] = False
        self.df['Sell'] = False

        for index, row in self.df.iterrows():
            if row['Signal'] == 1 and position == 0:  
                position = 1
                buy_price = row['Close']
                buy_date = row['Date']
                shares = self.capital / buy_price
                self.capital = 0
                self.df.loc[index, 'Buy'] = True
                print(f"Buy: {buy_date} | Price: ${buy_price:.2f}")
            elif row['Signal'] == -1 and position == 1:  
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
        d = display.Display(self.stock)
        d.generateMovingAverageCrossoverGraph(self.getData(),self.slow,self.fast)
        return