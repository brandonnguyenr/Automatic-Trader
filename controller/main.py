import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadData as dd
from Display import Display as display
from movingAverageCrossover import MovingAverageCrossover as mva
from bollingerBandBounce import BollingerBandBounce as bb

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
    
def inputETF():
    while True:
        result = input("Enter ETF (FNGD/FNGU): ")
        if result.isalpha() and result == "FNGD" or result == "FNGU":
            result = result.upper()
            return result
        else:
            print("Invalid! Try again")

def validDate(date):
    try:
        from datetime import datetime
        datetime.strptime(date, '%m%d%Y')
        return True
    except ValueError:
        return False
    
def inputDate(message):
    while True:
        result = input(message)
        if result.isnumeric() == False:
            print("Invalid! Try again.")
            continue
        if result.isnumeric() and validDate(result):
            return result
        else:
            print("Invalid! Try again.")

def validRange(date1,date2):
    dateFormat = "%m%d%Y"
    dt1 = datetime.strptime(date1,dateFormat)
    dt2 = datetime.strptime(date2,dateFormat)

    if dt1 > dt2:
        return False
    else:
        return True
    
def inputWindow(message):
    print("\nFor default value enter non numeric values")
    result = input(message)
    if result.isnumeric() == True:
        return int(result)
    else:
        return -1
        
def backtestInterface():
    while True:
        user = input("1. Moving Average Crossover\n2. Bollinger Band Bounce\nR. Return\nChoice: ")
        if user == "1":
            etf = inputETF()
            date1 = inputDate("Enter start date (MMDDYYYY): ")
            date2 = inputDate("Enter end date (MMDDYYYY): ")
            if validRange(date1,date2) == False:
                print("Invalid range! Try again\n")
                continue

            fast_window = inputWindow("Enter fast window range: ") 
            if fast_window == -1:
                fast_window = 7
            slow_window = inputWindow("Enter slow window range: ")
            if slow_window == -1:
                slow_window = 30
            date1 = calculateDaysBefore(date=date1,daysBefore=slow_window)
            stock = dd(etf,date1,date2)
            # test = bt(stock,date1,date2)
            # test.testMovingAverageCrossover(slow_window=slow_window,fast_window=fast_window)
            test = mva(stock,date1,date2,slow=slow_window,fast=fast_window)
            test.testStrategy()

        elif user == "2":
            etf = inputETF()
            date1 = inputDate("Enter start date (MMDDYYYY): ")
            date2 = inputDate("Enter end date (MMDDYYY): ")
            # if validRange(date1,date2) == False:
            #     print("Invalid range! Try again\n")
            #     continue
            window = inputWindow("Enter window range: ")
            if window == -1:
                window = 15
            date1 = calculateDaysBefore(date=date1,daysBefore=window)
            stock = dd(etf,date1,date2)
            # test = bt(stock,date1,date2)
            # test.testBollingerBandBounce(window=window)
            test = bb(stock,date1,date2,window=window)
            test.testStrategy()
        elif user.lower() == "r":
            break

        else:
            print("Invalid try again")

def historicalGraphInterface():
    while True:
                user = input("Which graph would you like to view?\n1. FNGD\n2. FNGU\nR. Return\nChoice: ")
                if user == "1":
                    date1 = inputDate("Enter start date (MMDDYYYY): ")
                    date2 = inputDate("Enter end date (MMDDYYYY): ")
                    if validRange(date1,date2) == False:
                        print("Invalid range! Try again\n")
                        continue
                    stock = dd('FNGD', date1, date2)
                    d = display(stock)
                    d.generateHistoricalGraph()
                elif user == "2":
                    date1 = inputDate("Enter start date (MMDDYYYY): ")
                    date2 = inputDate("Enter end date (MMDDYYYY): ")
                    if validRange(date1,date2) == False:
                        print("Invalid range! Try again\n")
                        continue
                    
                    stock = dd('FNGU', date1, date2)
                    d = display(stock)
                    d.generateHistoricalGraph()
                elif user.lower() == "r":
                    break
                else:
                    print("Invalid try again")
                    
def main():
    print("*****Welcome to FN Trader*****")

    while True:
        print("What would you like to do?")
        user = input("1. View historical stock graph\n2. Backtest trading strategies\nQ. Quit\nChoice: ")
        if user == "1":
            historicalGraphInterface()
        elif user == "2":
            backtestInterface()
        elif user.lower() == "q":
            quit()
        else:
            print("Invalid input, try again!")

if __name__ == "__main__":
    main()