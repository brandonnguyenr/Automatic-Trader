import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadData as dd
from Display import Display as display
from Backtest import Backtest as bt

def calculateDaysBefore(date,daysBefore):
    try:
        # Parse the input date string into a datetime object
        date_format = "%m%d%Y"
        input_date = datetime.strptime(date, date_format)

        # Calculate the date x days before the input date
        days_delta = timedelta(days=daysBefore)
        result_date = input_date - days_delta

        # Convert the result date to MMDDYYYY format
        result_date_str = result_date.strftime(date_format)

        return result_date_str

    except ValueError:
        return "Invalid date format. Please use MMDDYYYY."

def main():
    print("*****Welcome to FN Trader*****")

    while True:
        print("What would you like to do?")
        user = input("1. View historical stock graph\n2. Backtest trading strategies\nQ. Quit\nChoice: ")
        if user == "1":
            while True:
                user = input("Which graph would you like to view?\n1. FNGD\n2. FNGU\nR. Return\nChoice: ")
                if user == "1":
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    stock = dd('FNGD', date1, date2)
                    d = display(stock)
                    d.generateHistoricalGraph()
                elif user == "2":
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    stock = dd('FNGU', date1, date2)
                    d = display(stock)
                    d.generateHistoricalGraph()
                elif user.lower() == "r":
                    break
                else:
                    print("Invalid try again")

        elif user == "2":

            while True:
                user = input("1. Moving Average Crossover\n2. Bollinger Band Bounce\nR. Return\nChoice: ")
                if user == "1":
                    etf = input("Enter ETF (FNGD/FNGU): ")
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    fast_window = 7 
                    slow_window = 30  
                    date1 = calculateDaysBefore(date=date1,daysBefore=slow_window)
                    stock = dd(etf,date1,date2)
                    test = bt(stock,date1,date2)
                    test.testMovingAverageCrossover(slow_window=slow_window,fast_window=fast_window)

                elif user == "2":
                    etf = input("Enter ETF (FNGD/FNGU): ")
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    window = 15
                    date1 = calculateDaysBefore(date=date1,daysBefore=window)
                    stock = dd(etf,date1,date2)
                    test = bt(stock,date1,date2)
                    test.testBollingerBandBounce(window=window)

                elif user.lower() == "r":
                    break

                else:
                    print("Invalid try again")

        elif user.lower() == "q":
            quit()

        else:
            print("Invalid input, try again!")

if __name__ == "__main__":
    main()