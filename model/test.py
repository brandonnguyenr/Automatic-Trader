import unittest
import os
import sys
from datetime import datetime
import pandas as pd
# Append the path to the parent directory of 'model' and 'view'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadDataAdaptee as dd
from bollingerBandBounce import BollingerBandBounce as bb

class TestSum(unittest.TestCase):
    
    def test_dateTimeObjects(self):
        stock = dd('FNGD', '01252023', '07252023')
        for data in stock.getDate():
            assert isinstance(data,datetime) == True, "Should be date time object"
        return
    
    def test_integration(self):
        date1 = '01252023'
        date2 = '07252023'
        stock = dd('FNGD', date1, date2)
        bandbounce = bb(stock,date1,date2,15)
        assert isinstance(bandbounce.getData(),pd.DataFrame) == True, "should be pandas array"
        return

if __name__ == "__main__":
    unittest.main()