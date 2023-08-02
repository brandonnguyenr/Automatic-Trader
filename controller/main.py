import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadData as dd
from Display import Display as display
from movingAverageCrossover import mva
from bollingerBandBounce import bollingerBB

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
                    d.generateGraph()
                elif user == "2":
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    stock = dd('FNGU', date1, date2)
                    d = display(stock)
                    d.generateGraph()
                elif user.lower() == "r":
                    break
                else:
                    print("Invalid try again")

        elif user == "2":
            while True:
                user = input("1. Moving Average Crossover\n2. Bollinger Band Bounce\nR. Return\nChoice: ")
                if user == "1":
                    mva()
                elif user == "2":
                    bollingerBB()
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