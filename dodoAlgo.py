import socket
import sys


def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        toReturn = ""
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
    for i in range(len(securityInfos) / 4):
        testDict = {
            "ticker": securityInfos[i * 4],
            "net_worth": securityInfos[i * 4 + 1],
            "dividend_ratio": securityInfos[i * 4 + 2],
            "volatility": securityInfos[i * 4 + 3]
        }
        securityDict.append(testDict)
    return securityDict

def getAllTickers():
    securityInfos = run("Dodo", "pie", "SECURITIES")
    securityInfos = securityInfos.split(' ')
    securityInfos = securityInfos[1:]
    tickers = []
    for i in range(len(securityInfos) / 4):
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



def executeBuy(stockTuple):
    ticker = stockTuple[0]
    price = stockTuple[1]

    myOrdersDict = getMyOrdersDict()
    if myOrdersDict is not None:
        for dic in myOrdersDict:
            if dic["status"] == "BID" and dic["ticker"] == ticker:
                return 0



    ordersDict = getOrdersDict(ticker)
    print(ordersDict[0])
    myMoney = float(shortRun("MY_CASH").split(' ')[1: ][0])
    for dic in ordersDict:
        if dic["status"] == "ASK" and dic["price"] >= price:
            amountToBuy = myMoney//price
            if amountToBuy > dic["numStocks"]:
                amountToBuy = dic["numStocks"]
            shortRun("BID " + ticker + " " + str(price + 1) + " " + str(amountToBuy))


def getAllAsks(ticker):
    orders = run("Dodo", "pie", "ORDERS " + str(ticker))
    print orders
    orders = orders.split(' ')
    orders = orders[1:]
    pricesOfAsks = []
    for i in range(len(orders) / 4):
        if orders[i * 4] == "ASK":
            pricesOfAsks.append(float(orders[i * 4 + 2]))
    return pricesOfAsks

def goodBargain():
    securities = getSecurityDict()
    bestRatio = None
    bestCur = None
    for security in securities:
        print security['ticker']
        marketVal = float(security['net_worth'])
        dividendRatio = float(security['dividend_ratio'])
        for price in getAllAsks(security['ticker']):
            if (bestRatio is None) or ((marketVal / price) * dividendRatio > bestRatio):
                bestRatio = (marketVal / price) * dividendRatio
                bestCur = (security['ticker'], price)
    print bestRatio
    return bestCur

try:
    print goodBargain()
except:
    e = sys.exc_info()[0]
    print ("error " + str(e))
    run("Dodo", "pie", "CLOSE_CONNECTION")

