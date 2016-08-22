import tkinter as tk
from tkinter import ttk
from Algs import *

def getPrice(chosenStock):
    """
    Retrieves the last trade price of a stock.

    :param chosenStock: stock symbol
    :return: float value of last trade price
    """

    allInfo = getQuotes(chosenStock)
    theStock = allInfo[0]
    price = theStock["LastTradePrice"]
    return price

with open('Dow30.txt', 'r') as Dow30:
    Dow30List = []
    for line in Dow30:
        for word in line.split():
            Dow30List.append(word)

def createListofStocksForDow(list):

    prices = {}

    for stock in list:

        stockPrice = getPrice(chosenStock=stock)

        prices[stock] = stockPrice

    return prices

BIG_FONT = ('Comic Sans MS', 20)


class TSXSharemarketApp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Settings, MainSMPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="TOMS STOCK EXCHANGE", font=BIG_FONT)
        Title.grid(row=0, rowspan=3, columnspan=6)

        Dow = tk.Label(self, text=("DOW: " + str(getPrice(chosenStock=".DJI"))))
        Dow.grid(row=4, columnspan=2)

        AAPL = tk.Label(self, text=("AAPL: " + str(getPrice(chosenStock="AAPL"))))
        AAPL.grid(row=4, column=2, columnspan=2)

        Goog = tk.Label(self, text=("GOOG: " + str(getPrice(chosenStock="GOOG"))))
        Goog.grid(row=4, column=4, columnspan=2)

        SmGo = ttk.Button(self, text="Sharemarket", command=lambda: controller.show_frame(MainSMPage))
        SmGo.grid(row=5, columnspan=2)

        Setting = ttk.Button(self, text="Settings", command=lambda: controller.show_frame(Settings))
        Setting.grid(row=5, column=2, columnspan=2)

        Quit = ttk.Button(self, text="Quit", command=lambda: quit())
        Quit.grid(row=5, column=4, columnspan=2)


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Settings", font=BIG_FONT)
        Title.grid(row=0, rowspan=3, columnspan=6)

        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=4, columnspan=2)


class MainSMPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        Markets = [
            "*Please Select A Market",
            "DOW JONES",
            "NASDAQ",
            "ASX"
        ]

        selectedMarketL = tk.StringVar()

        SelectMarket = ttk.OptionMenu(self, selectedMarketL, *Markets)
        SelectMarket.grid(row=0, column=0, columnspan=1)

        MarketNameGo = ttk.Button(self, text="GO", command=lambda: self.changeFrame(controller))
        MarketNameGo.grid(row=0, column=4, columnspan=2)

        bsmenu = ttk.Button(self, text="Buy / Sell Menu")
        bsmenu.grid(row=8, column=5, columnspan=3, rowspan=3)

        vp = ttk.Button(self, text="View Portfolio")
        vp.grid(row=16, column=5, columnspan=3, rowspan=3)

        gb = ttk.Button(self, text="Go Back Home")
        gb.grid(row=24, column=5, columnspan=3, rowspan=3)

    def changeFrame(self, controller):

        prices = createListofStocksForDow(Dow30List)

        nameVars = dict()

        num = 1

        numRow = 3

        for stock in prices:

            num = num + 1

            nameVars[stock] = "Label" + str(num)

        for stockName in nameVars:

            numRow = numRow + 1

            nameVars[stockName] = tk.Label(self, text=stockName + '  :  ' + str(prices[stockName]))\
                .grid(row=numRow, column=0, columnspan=1)

app = TSXSharemarketApp()

app.geometry("800x800+0+0")

menu = tk.Menu(app)
app.config(menu=menu)

subMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New")
subMenu.add_command(label="Save")
subMenu.add_separator()
subMenu.add_command(label="Settings")
subMenu.add_separator()
subMenu.add_command(label="Exit", command=lambda: quit())

app.mainloop()