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

def shortRun(command):
    run("Dodo", "pie", command)


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

def getAllTickers():
    securityInfos = run("Dodo", "pie", "SECURITIES")
    securityInfos = securityInfos.split(' ')
    securityInfos = securityInfos[1:]
    tickers = []
    for i in range(len(securityInfos) / 4):
        tickers.append(securityInfos[i * 4])
    return tickers

def getoOrdersDict(ticker):
    orders = shortRun()

def executeBuy(stockTuple):
    ticker = stockTuple[0]
    price = stockTuple[1]

def goodBargain():
    print "Ashay"

try:
    securityInfos = getSecurityDict()
except:
    print ("error")
    run("Dodo", "pie", "CLOSE_CONNECTION")
