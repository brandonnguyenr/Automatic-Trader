import unittest
import os
import sys

# Append the path to the parent directory of 'model' and 'view'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadData as dd

class TestSum(unittest.TestCase):
    
    def test_Downloads(self):
        stock = dd('FNGD', '07252020', '07252023')
        stock2 = dd('FNGU', '07252020', '07252023')

        self.assertEqual(len(stock.getClose()), len(stock2.getClose()))

        stock2 = dd('FNGU', '07252020', '07262023')
        self.assertNotEqual(len(stock.getClose()), len(stock2.getClose()))

if __name__ == "__main__":
    unittest.main()