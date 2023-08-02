
import matplotlib.pyplot as plt


class Display:
    def __init__(self,stock):
        self.stock = stock

    def generateGraph(self):

        xpoints = self.stock.getDate()
        ypoints = self.stock.getClose()

        plt.plot(xpoints,ypoints, label = self.stock.getName())
        plt.legend(loc='upper right')
        #not required but included to ensure formatting.
        plt.gcf().autofmt_xdate()


        """ code below uncomment if x-axis to show only years
        """
        # date_format = mdates.DateFormatter('%Y')
        # plt.gca().xaxis.set_major_formatter(date_format)
        plt.xlabel('Date')
        plt.ylabel('Close USD')
        plt.title(self.stock.getName())
        plt.show()