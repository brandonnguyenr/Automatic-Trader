
import matplotlib.pyplot as plt

class Display:
    def __init__(self,stock):
        self.stock = stock

    def generateHistoricalGraph(self):
        xpoints = self.stock.getDate()
        ypoints = self.stock.getClose()

        plt.plot(xpoints,ypoints, label = self.stock.getName())
        plt.legend(loc='upper right')
        #not required but included to ensure formatting.
        plt.gcf().autofmt_xdate()


        #code below uncomment if x-axis to show only years
        # date_format = mdates.DateFormatter('%Y')
        # plt.gca().xaxis.set_major_formatter(date_format)
        plt.xlabel('Date')
        plt.ylabel('Close USD')
        plt.title(self.stock.getName())
        plt.show()

    def generateBollingerBBGraph(self,df):
        window = 15
        xpoints = self.stock.getDate()
        ypoints = self.stock.getClose()

        plt.figure(figsize=(12, 6))
        plt.plot(xpoints, ypoints, label='Closing Prices', color='blue')

        plt.plot(xpoints, df['MA'], label=f'{window}-day MA', color='orange')
        plt.fill_between(xpoints, df['Upper'], df['MA'], alpha=0.2, color='green', label='Upper Bollinger Band')
        plt.fill_between(xpoints, df['MA'], df['Lower'], alpha=0.2, color='red', label='Lower Bollinger Band')

        # Add buy/sell points to the graph
        plt.scatter(df[df['Buy'] == True]['Date'], df[df['Buy'] == True]['Close'], marker='^', color='g', label='Buy', lw=0)
        plt.scatter(df[df['Sell'] == True]['Date'], df[df['Sell'] == True]['Close'], marker='v', color='r', label='Sell', lw=0)

        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.title('Bollinger Band Bounce Trading Strategy')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.show()

    def generateMovingAverageCrossoverGraph(self,df,slow_window,fast_window):
        xpoints = self.stock.getDate()
        ypoints = self.stock.getClose()

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

