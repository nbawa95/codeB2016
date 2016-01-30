import socket
import sys
import random

def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    toReturn = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            toReturn += rline.strip()
            rline = sfile.readline()
    finally:
        sock.close()
        return toReturn

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()


def getSecurityDict():
    securityInfos = run("Dodo", "pie", "SECURITIES")
    securityInfos = securityInfos.split(' ')
    securityInfos = securityInfos[1:]
    securityDict = []
    for i in range(len(securityInfos) // 4):
        testDict = {
            "ticker": securityInfos[i * 4],
            "net_worth": securityInfos[i * 4 + 1],
            "dividend_ratio": securityInfos[i * 4 + 2],
            "volatility": securityInfos[i * 4 + 3]
        }
        securityDict.append(testDict)
    return securityDict

def getMySecurityDict():
    mySecurityInfos = run("Dodo", "pie", "MY_SECURITIES")
    mySecurityInfos = mySecurityInfos.split(' ')
    mySecurityInfos = mySecurityInfos[1:]
    #print mySecurityInfos
    mySecurityDict = []
    for i in range(len(mySecurityInfos) / 3):
        testDict = {
            "ticker": mySecurityInfos[i * 3],
            "shares": mySecurityInfos[i * 3 + 1],
            "dividend_ratio": mySecurityInfos[i * 3 + 2],
        }
        #print testDict
        mySecurityDict.append(testDict)
    print (mySecurityDict)
    return mySecurityDict


def getAllTickers():
    securityInfos = run("Dodo", "pie", "SECURITIES")
    securityInfos = securityInfos.split(' ')
    securityInfos = securityInfos[1:]
    tickers = []
    for i in range(len(securityInfos) // 4):
        tickers.append(securityInfos[i * 4])
    return tickers

def shortRun(command):
    return run("Dodo", "pie", command)


def getOrdersDict(ticker):
    orders = shortRun("ORDERS " + ticker)
    orders = orders.split(' ')
    orders = orders[1:]
    ordersDict = []
    for i in range(len(orders) // 4):
        testDict = {
            "status": orders[i*4],
            "ticker": orders[i * 4 + 1],
            "price": float(orders[i * 4 + 2]),
            "numStocks": int(orders[i * 4 + 3])
        }
        ordersDict.append(testDict)
    return ordersDict

def getMyOrdersDict():
    myOrders = shortRun("MY_ORDERS")
    if myOrders == None:
        return None
    myOrders = myOrders.split(' ')[1:]
    myOrdersDict = []
    for i in range(len(myOrders) // 4):
        testDict = {
            "status": myOrders[i*4],
            "ticker": myOrders[i * 4 + 1],
            "price": float(myOrders[i * 4 + 2]),
            "numStocks": int(myOrders[i * 4 + 3])
        }
        myOrdersDict.append(testDict)
    return myOrdersDict

def getAllAsks(ticker):
    orders = run("Dodo", "pie", "ORDERS " + str(ticker))
    #print orders
    orders = orders.split(' ')
    orders = orders[1:]
    pricesOfAsks = []
    for i in range(len(orders) // 4):
        if orders[i * 4] == "ASK":
            pricesOfAsks.append(float(orders[i * 4 + 2]))
    return pricesOfAsks


def executeBuy(stockTuple):
    if stockTuple is None:
        print("Stock tuple is none")
        return 0
    ticker = stockTuple[0]
    price = stockTuple[1]



    ordersDict = getOrdersDict(ticker)
    myMoney = float(shortRun("MY_CASH").split(' ')[1: ][0])
    for dic in ordersDict:
        if dic["status"] == "ASK" and dic["price"] >= price:
            amountToBuy = myMoney//price

            if amountToBuy > dic["numStocks"]:
                amountToBuy = dic["numStocks"]
            print("double passed " + str(amountToBuy) + " " + ticker)
            print("BID " + ticker + " " + str(price) + " " + str(amountToBuy))
            print(shortRun("BID " + ticker + " " + str(price) + " " + str(int(amountToBuy))))

    myOrdersDict = getMyOrdersDict()
    r = random.random()
    if myOrdersDict is not None:
        print("passed")
        for dic in myOrdersDict:
            if dic["status"] == "BID" and dic["ticker"] == ticker and r >=0.5:
                print(shortRun("CLEAR_BID " + ticker))
                

def getAllBids(ticker):
    orders = run("Dodo", "pie", "ORDERS " + str(ticker))
    #print orders
    orders = orders.split(' ')
    orders = orders[1:]
    pricesOfBids = []
    for i in range(len(orders) / 4):
        if orders[i * 4] == "BID":
            pricesOfBids.append(float(orders[i * 4 + 2]))
        #print pricesOfBids
    return pricesOfBids

def checkDesperate():
    threshhold = 0.0001
    mySecurities = getMySecurityDict()
    for security in mySecurities:
        dividendRatio = float(security["dividend_ratio"])
        shares = int(security["shares"])
        ticker = security["ticker"]
        if (dividendRatio <= threshhold and shares > 0):
            #print "this is the one we should sell "+ ticker
            allBids = getAllBids(ticker)
            if len(allBids) != 0:
                maxPrice = allBids[0]
                for price in allBids:
                    if maxPrice < price:
                        maxPrice = price
                #print "maxprice" + str(maxPrice)
                askCommand = "ASK " + ticker + " " + str(maxPrice) + " " + str(int(shares))
                print(run("Dodo", "pie", askCommand))
                #print ("end")

def goodBargain():
    securities = getSecurityDict()
    bestRatio = None
    bestCur = None
    for security in securities:
        #print security['ticker']
        marketVal = float(security['net_worth'])
        dividendRatio = float(security['dividend_ratio'])
        for price in getAllAsks(security['ticker']):
            if (bestRatio is None) or ((marketVal / price) * dividendRatio > bestRatio):
                bestRatio = (marketVal / price) * dividendRatio
                bestCur = (security['ticker'], price)
    #print bestRatio
    return bestCur

def iHaveMoney():
    return (float(run("Dodo", "pie", "MY_CASH").split(" ").pop()) > 0)

try:
    while True:
        if iHaveMoney:
            yo = goodBargain()
            executeBuy(yo)
            if yo is not None:
                print(shortRun("ORDERS " + yo[0]))
            print(shortRun("MY_SECURITIES"))
            print(shortRun("MY_ORDERS"))
            print(shortRun("MY_CASH"))
        checkDesperate()
        subscribe("Dodo", "pie")
except:
    e = sys.exc_info()[0]
    print ("error " + str(e))
    run("Dodo", "pie", "CLOSE_CONNECTION")