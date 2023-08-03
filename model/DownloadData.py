import time
import datetime
import pandas as pd
import numpy as np
import json 

class DownloadData:
    def __init__(self,symbol,dateStart,dateEnd):
        """constructor for DownloadData, the purpose of this class is to access the yahoo finance api to get ETF historical stock data. Then it will download it to the local machine. 
        Creates an object of the downloaded stock data.

        Args:
            symbol (str): ETF symbol, i.e. FNGD/FNGU
            dateStart (str): starting date range; format should be YYYYMMDD no spaces no dashes 
            dateEnd (str): ending date range; format should be YYYYMMDD no spaces no dashes
        """
        self._symbol = symbol

        self.startYear = int(dateStart[-4:])
        self.startDay = int(dateStart[2:4])
        self.startMonth = int(dateStart[:2])

        self.endMonth = int(dateEnd[:2])
        self.endDay = int(dateEnd[2:4])
        self.endYear = int(dateEnd[-4:])

        self._csvdata, self._data = self._getData()

        

    def _getData(self):
        """_summary_

        Returns:
            dict: returns a dict that contains historical stock information such as high, low, close, open, & date
        """
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
        """Purpose of this is to be used in Display.py which will be the y-axis coordinates.

        Returns:
            array: returns an array containing the closing values per day
        """
        return np.fromiter(self._data['Close'].values(), dtype=float)

    def getDate(self):
        """The array contains the dates which will be used in Display.py as the x-axis coordinates.

        Returns:
            array: each element is of the date time object from the datetime class.
        """
        arr = []
        for d in self._data['Date']:
            date = datetime.datetime.strptime(self._data['Date'][d], "%Y-%m-%d")
            arr.append(date)
        return arr

    def getName(self):
        return self._symbol
    
    def getCSV(self):
        """ to get the CSV dataframe for pandas functions

        Returns:
            pandas object dataframe
        """
        return self._csvdata