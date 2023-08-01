import unittest
import DownloadData as dd
import os

class TestSum(unittest.TestCase):
    
    def test_Downloads(self):
        stock = dd.DownloadData('FNGD','07252020','07252023')
        stock2 = dd.DownloadData('FNGU','07252020','07252023')

        self.assertEqual(len(stock.getClose()), len(stock2.getClose()))

        stock2 = dd.DownloadData('FNGU','07252020','07262023')
        self.assertNotEqual(len(stock.getClose()), len(stock2.getClose()))

if __name__ == "__main__":
    unittest.main()