import tkinter as tk
from tkinter import ttk
from Algs import *
import threading
from queue import Queue
import urllib.request

#ALGORITHMS FROM VERSION 1

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

def getOHCL(chosenStock):

    baseUrl = "http://finance.yahoo.com/d/quotes.csv?s=" + str(chosenStock) + "&f=c1"

    with urllib.request.urlopen(baseUrl) as response:
        data = response.read()

    if str('+') in str(data):
        return "UpArrow.png"
    else:
        return "DownArrow.png"

def getChange(chosenStock):
    baseUrl = "http://finance.yahoo.com/d/quotes.csv?s=" + str(chosenStock) + "&f=c1"

    with urllib.request.urlopen(baseUrl) as response:
        data = response.read()

    if str('+') in str(data):
        return "Positive"
    else:
        return "Negative"

# Dow Algorithms
def getDow():

    with open("TempDow.txt", 'r') as Dow:

        dowstring = str(Dow.read())
        DowPrices = eval(dowstring)

    return DowPrices


# INITIALISE DEFAULTS

with open('stocksBought.txt', 'r') as stockFile:

    stockstring = str(stockFile.read())
    stocksBought = eval(stockstring)


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

    with open("TempDow.txt", 'w') as DowDict:

        DowDict.write(str(prices))

    print("Done")

    return prices


def createChangeDow(list):

    changeDow = {}

    prices = list

    for stockName in prices:

        changeDow[stockName] = getOHCL(chosenStock=stockName)

    with open("TempChangeDow.txt", 'w') as change:

        change.write(str(changeDow))

    print("Done")

def getChangeDictDow():

    with open("TempChangeDow.txt", 'r') as change:

        changeString = str(change.read())
        DowChange = eval(changeString)

    return DowChange

q = Queue()

t = threading.Thread(target=createListofStocksForDow, args=[Dow30List])
t.daemon = True
t.start()

t2 = threading.Thread(target=createChangeDow, args=[Dow30List])
t2.daemon = True
t2.start()

BIG_FONT = ('Impact', 20)
BIG_BIG_FONT = ('Impact', 35)
MEDIUM_FONT = ('Times New Roman', 18)

balance = 50000

#GUI PART BEGINS


class TSXSharemarketApp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Settings, MainSMPage, CheckStock, buySellMenuStartPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="NSEW")

            frame.configure(bg="#F0F0F0")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="TOMS STOCK EXCHANGE", font=BIG_BIG_FONT)
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
        SelectMarket.grid(row=0, column=0, columnspan=3)

        MarketNameGo = ttk.Button(self, text="GO")
        MarketNameGo.grid(row=0, column=4, columnspan=2)

        bsmenu = ttk.Button(self, text="Buy / Sell Menu", command=lambda: controller.show_frame(buySellMenuStartPage))
        bsmenu.grid(row=8, column=5, columnspan=13, rowspan=3)

        cs = ttk.Button(self, text="Check A Stock - Done)", command=lambda: controller.show_frame(CheckStock))
        cs.grid(row=16, column=5, columnspan=13, rowspan=3)

        vp = ttk.Button(self, text="Tets")
        vp.grid(row=24, column=5, columnspan=13, rowspan=3)

        gb = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        gb.grid(row=30, column=5, columnspan=13, rowspan=3)

        prices = getDow()

        nameVars = dict()

        num = 1

        numRow = 3

        for stock in prices:

            num = num + 1

            nameVars[stock] = "Label" + str(num)

        for stockName in nameVars:

            numRow = numRow + 1

            nameVars[stockName] = tk.Label(self, text=stockName + (" |")).grid(row=numRow, column=0, columnspan=1, sticky='E')

        numRow2 = 3

        for stockName in nameVars:
            numRow2 = numRow2 + 1

            nameVars[stockName] = tk.Label(self, text=(" ") + prices[stockName]).grid(row=numRow2, column=1, columnspan=1,
                                                                               sticky='W')


class CheckStock(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        main = tk.Label(self, text="Enter Stock Symbol: ", font=BIG_BIG_FONT)
        main.grid(row=0, columnspan=5)

        enterstock = ttk.Entry(self)
        enterstock.grid(row=1, column=1)

        priceLbl = tk.Label(self, font=BIG_FONT)

        priceLbl.grid(row=2, column=1)

        ok = ttk.Button(self, text="GO", command=lambda: self.displayPrice(controller, enterstock.get(), priceLbl))
        ok.grid(row=1, column=2)

    def displayPrice(self, controller, stock, priceLbl):

        chosenStock = str(stock)

        price = str(getPrice(chosenStock))

        priceLbl['text'] = chosenStock + " : " + price

class buySellMenuStartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        main = tk.Label(self, text="Buy / Sell Menu", font=BIG_BIG_FONT)
        main.grid(row=0, columnspan=5)

        slbl =  tk.Label(self, text="Sell", font=BIG_FONT)
        slbl.grid(row=2, column=5)

        home = ttk.Button(self, text="Home", command=lambda: controller.show_frame(MainSMPage))
        home.grid(row=0, column=5)

        numRow = 2

        for stock in stocksBought:

            numRow = numRow + 1

            tk.Label(self, text=(stock), font=MEDIUM_FONT).grid(row=numRow, column=4, sticky='e')

            tk.Label(self, text=("|  " + str(stocksBought[stock])), font= MEDIUM_FONT).grid(row=numRow, column=5, sticky='w')

            ttk.Button(self, text="Sell",).grid(row=numRow, column=6, sticky='w')

app = TSXSharemarketApp()

app.geometry("800x800+0+0")

menu = tk.Menu(app)
app.config(menu=menu)
app.title("Toms Stock Exchange")

subMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New")
subMenu.add_command(label="Save")
subMenu.add_separator()
subMenu.add_command(label="Settings")
subMenu.add_separator()
subMenu.add_command(label="Exit", command=lambda: quit())

editMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Home")

toolbar = tk.Frame(app)
# - Dow Jones Status
b = tk.Label(toolbar, text="Dow Jones: " + str(getPrice(chosenStock=".DJI")))
b.grid()
# - Get Image For Change
bArrowImg = tk.PhotoImage(file=str(getOHCL("DOW")))
bArrowLbl = tk.Label(toolbar, image=bArrowImg)
bArrowLbl.grid(row=0, column=2)
# - ASX Status
a = tk.Label(toolbar, text="  |    ASX 200: " + str(getPrice(chosenStock='XJO')))
a.grid(row=0, column=3)
# - Get Image For Change
aArrowImg = tk.PhotoImage(file=str(getOHCL("^AXJO")))
aArrowLbl = tk.Label(toolbar, image=aArrowImg)
aArrowLbl.grid(row=0, column=4)

spaces = tk.Label(toolbar, text="                                                  "
                                "                                                  "
                                "                                                 | Balance: " + str(balance))
spaces.grid(row=0, column=5)


toolbar.pack(side='top', fill='x')

app.mainloop()