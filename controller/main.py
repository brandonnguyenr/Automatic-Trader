""" 
Program name: "FN Trader"

Authors: Kevin Nguyen, Brandon Nguyen

TODOs: need to refactor code 
"""

import os
import sys

# Append the path to the parent directory of 'model' and 'view'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'view')))

from DownloadData import DownloadData as dd
from Display import Display as display
from movingAverageCrossover import mva
from bollingerBandBounce import bollingerBB

def main():
    print("*****Welcome to FN Trader*****")
    user = "12"
    """
        first loop for entire program
        Choices:
            1. View historical stock graph
            2. Backtest trading strategies
            Q. end program
    """
    while True:
        print("What would you like to do?")
        user = input("1. View historical stock graph\n2. Backtest trading strategies \nQ. Quit\nChoice: ")
        if user == "1":

            """
                inner loop one for viewing just historical stock data
            """
            while True:
                user = input("Which graph would you like to view?\n1. FNGD\n2. FNGU\nR. Return\nChoice:")
                if user == "1":
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    stock = dd.DownloadData('FNGD',date1,date2)
                    d = display.Display(stock)
                    d.generateGraph()
                if user == "2":
                    date1 = input("Enter start date (MMDDYYYY): ")
                    date2 = input("Enter end date (MMDDYYYY): ")
                    stock = dd.DownloadData('FNGU',date1,date2)
                    d = display.Display(stock)
                    d.generateGraph()
                elif user == "R" or user == "r":
                    break
                else:
                    print("Invalid try again")
                

        elif user == "2":
            """
                inner loop two for viewing backtesting strategy graphs against historical stock data.
            """
            while True:
                user = input("1. Moving Average Crossover\n2. Bollinger Band Bounce\nR. Return \nChoice: ")
                if user == "1":
                    mva()
                elif user == "2":
                    bollingerBB()
                elif user == "R" or user == "r":
                    break
                else:
                    print("Invalid try again")
        elif user == "q" or user == "Q":
            quit()
        else:
            print("invalid input try again!")

if __name__ == "__main__":
    main()
