import time
import datetime
import pandas as pd
import numpy as np
import json 

class DownloadDataAdaptee:
    def __init__(self,symbol,dateStart,dateEnd):
        # constructor for DownloadData, the purpose of this class is to access the yahoo finance api to get ETF historical stock data. Then it will download it to the local machine. 
        # Creates an object of the downloaded stock data.

        # Args:
        #     symbol (str): ETF symbol, i.e. FNGD/FNGU
        #     dateStart (str): starting date range; format should be YYYYMMDD no spaces no dashes 
        #     dateEnd (str): ending date range; format should be YYYYMMDD no spaces no dashes
        
        self._symbol = symbol

        self.startYear = int(dateStart[-4:])
        self.startDay = int(dateStart[2:4])
        self.startMonth = int(dateStart[:2])

        self.endMonth = int(dateEnd[:2])
        self.endDay = int(dateEnd[2:4])
        self.endYear = int(dateEnd[-4:])

        #The data below is the adaptee. The adapter is the display class which requires the CSV data. While the date and close information
        #requires JSON formatted data. 
        self._csvdata, self._data = self._getData()

    
    def _getData(self):
        # For obtaining data, it should not be used outside of this class.

        # Returns:
        #     dict: returns a dict that contains historical stock information such as high, low, close, open, & date
        
        ticker = self._symbol
        period1 = int(time.mktime(datetime.datetime(self.startYear, self.startMonth, self.startDay, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime(self.endYear, self.endMonth, self.endDay, 23, 59).timetuple()))
        interval = '1d' 

        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        df = pd.read_csv(API_endpoint)
        dict = df.to_dict()

        with open(f"{self._symbol}.json", "w") as file:
            json.dump(dict, file)

        return df,dict

    def getClose(self):
        # Purpose of this is to be used in Display.py which will be the y-axis coordinates.

        # Returns:
        #     array: returns an array containing the closing values per day
        
        return np.fromiter(self._data['Close'].values(), dtype=float)

    def getDate(self):
        # The array contains the dates which will be used in Display.py as the x-axis coordinates.

        # Returns:
        #     array: each element is of the date time object from the datetime class.
        
        arr = []
        for d in self._data['Date']:
            date = datetime.datetime.strptime(self._data['Date'][d], "%Y-%m-%d")
            arr.append(date)
        return arr

    def getName(self):
        return self._symbol
    
    def getCSV(self):
        #  to get the CSV dataframe for pandas functions

        # Returns:
        #     pandas object dataframe
        
        return self._csvdata

#AverageClosingPriceDecorator is a Decorator to the DownloadDataAdaptee class
#   It extends the functionality of DownloadDataAdaptee by using forward calls
#   to the original methods fo the adaptee
#   The extended functionality is calculating the average closing price of a listed time period
class AverageClosingPriceDecorator:
    def __init__(self, adaptee):
        self._adaptee = adaptee

    def calculate_average_closing_price(self):
        # Calculate the average closing price
        closing_prices = self._adaptee.getClose()
        average_closing_price = np.mean(closing_prices)
        return average_closing_price

    def getClose(self):
        # Call the original getClose method from the adaptee
        return self._adaptee.getClose()

    def getDate(self):
        # Call the original getDate method from the adaptee
        return self._adaptee.getDate()

    def getName(self):
        # Call the original getName method from the adaptee
        return self._adaptee.getName()

    def getCSV(self):
        # Call the original getCSV method from the adaptee
        return self._adaptee.getCSV()