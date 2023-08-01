import DownloadData as dd
import Display as display

from movingAverageCrosssover import mva
from bollingerBandBounce import bollingerBB

def main():
    print("*****Welcome to FN Trader*****")
    user = ""

    while True:
        print("What would you like to do?")
        user = input("1.View historical stock graph\n2.Backtest trading strategies \nQ.Quit\nChoice: ")
        if user == "1":
            while True:
                user = input("Which graph would you like to view?\n1.FNGD\n2.FNGU\nR.Return\nChoice:")
                if user == "1":
                    stock = dd.DownloadData('FNGD','07252020','07252023')
                    d = display.Display(stock)
                    d.generateGraph()
                if user == "2":
                    stock = dd.DownloadData('FNGU','07252020','07252023')
                    d = display.Display(stock)
                    d.generateGraph()
                elif user == "R" or user == "r":
                    break
                else:
                    print("Invalid try again")
                

        elif user == "2":
            while True:
                user = input("1. Bollinger Band Bounce\n2. Moving Average Crossover\nR. Return Choice: ")
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
