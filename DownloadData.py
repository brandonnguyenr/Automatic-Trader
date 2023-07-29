import time
import datetime
import pandas as pd
import numpy as np

class DownloadData:
    def __init__(self,symbol,dateStart,dateEnd):
        self._symbol = symbol

        self.startYear = int(dateStart[-4:])
        self.startDay = int(dateStart[2:4])
        self.startMonth = int(dateStart[:2])

        self.endMonth = int(dateEnd[:2])
        self.endDay = int(dateEnd[2:4])
        self.endYear = int(dateEnd[-4:])

        self._data = self._getData()
        

    def _getData(self):
        ticker = self._symbol
        period1 = int(time.mktime(datetime.datetime(self.startYear, self.startMonth, self.startDay, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime(self.endYear, self.endMonth, self.endDay, 23, 59).timetuple()))
        interval = '1d' 

        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        df = pd.read_csv(API_endpoint)

        return df.to_dict()

    def getClose(self):
        return np.fromiter(self._data['Close'].values(), dtype=float)

    def getDate(self):
        return len(self._data['Date'])
    
    def _displayCSV(self):
        ticker = self._symbol
        period1 = int(time.mktime(datetime.datetime(self.startYear, self.startMonth, self.startDay, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime(self.endYear, self.endMonth, self.endDay, 23, 59).timetuple()))
        interval = '1d' 

        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

        df = pd.read_csv(API_endpoint)
        print(df)