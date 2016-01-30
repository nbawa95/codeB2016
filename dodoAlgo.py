import socket
import sys
    
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
    for i in range(len(securityInfos) / 4):
        testDict = {
            "ticker": securityInfos[i * 4],
            "net_worth": securityInfos[i * 4 + 1],
            "dividend_ratio": securityInfos[i * 4 + 2],
            "volatility": securityInfos[i * 4 + 3]
        }
        securityDict.append(testDict)
    print (securityDict)
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
    threshhold = 0.00003
    mySecurities = getMySecurityDict()
    for security in mySecurities:
        dividendRatio = float(security["dividend_ratio"])
        shares = float(security["shares"])
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
                run("Dodo", "pie", askCommand)
                #print ("end")




#def goodBargain():
    #print "Ashay"

try:
    #print (run("Dodo", "pie", "MY_SECURITIES"))
    #checkDesperate()
    #print (run("Dodo", "pie", "MY_ORDERS"))
    print (run("Dodo", "pie", "SECURITIES"))
    #print run("Dodo", "pie", "MY_CASH")
except:
    e = sys.exc_info()[0]
    print (e)
    run("Dodo", "pie", "CLOSE_CONNECTION")


