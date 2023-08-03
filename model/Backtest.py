import bollingerBandBounce as bb
import Display as display
import movingAverageCrossover as mva

class Backtest:
    def __init__(self,stock,date1,date2):
        self.date1 = date1
        self.date2 = date2
        self.stock = stock
        self.df = self.stock.getCSV()
        
    def testBollingerBandBounce(self,window):
        test = bb.BollingerBandBounce(self.stock,self.date1,self.date2,window=window)
        test.calculations()
        self.df = test.getData()
        test.displaySignals()
        d = display.Display(self.stock)
        d.generateBollingerBBGraph(self.df)

    def testMovingAverageCrossover(self,slow_window,fast_window):
        test = mva.MovingAverageCrossover(self.stock,self.date1,self.date2,slow=slow_window,fast=fast_window)
        test.calculations()
        df = test.getData()
        test.displaySignals()
        d = display.Display(self.stock)
        d.generateMovingAverageCrossoverGraph(df,slow_window=slow_window,fast_window=fast_window)

        
        

    
