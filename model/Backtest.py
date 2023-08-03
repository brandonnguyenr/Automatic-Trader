
class Backtest:
    def __init__(self,stock,date1,date2):
        #Class for backtesting and calling on the trading strategy classes
        self.date1 = date1
        self.date2 = date2
        self.stock = stock
        self.df = self.stock.getCSV()
        self.initialCapital = 100000
        self.capital = self.initialCapital
        self.profitMarginPercentage = 0
        self.finalProfitLoss = 0
    
    def getData(self):
        # Used to get the dataframe data which will be used for the graph

        # Returns:
        #     pandas: returns a pandas dataframe object
        return self.df

    def getCapital(self):
        return self.capital
    
    def getProfitLoss(self):
        return self.finalProfitLoss
    
    def getprofitMargin(self):
        return self.profitMarginPercentage