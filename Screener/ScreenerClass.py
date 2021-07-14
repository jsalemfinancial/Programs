from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.scanner import ScannerSubscription
import time
import queue
import threading

q = queue.Queue()
mQ = queue.Queue()

class Screener(EWrapper, EClient):
    Qing = False
    barData = []
    listT = []
    listE = []
    listS = []
    listP = []

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
    def connect(self, host, port, clientId):
        super().connect(host, port, clientId)
        time.sleep(1)
        if self.isConnected() == True:
            print("Conected!")
            self.reqMarketDataType(1)
        else:
            print("Not Connected!")
        return 
    def error(self, reqId, errorCode, errorString):
        if reqId == -1:
            return
        else:
            print("Error: ", reqId, " ", errorCode, " ", errorString)
    def mainQueue(self, reqId):
        mQ.put(reqId)

        while True:
            if self.Qing == True:
                time.sleep(1)
            else:
                mQ.task_done()
                return
    def historicalData(self, reqId, bar):
        self.barData.append(bar.close)
        return super().historicalData(reqId, bar)
    def historicalDataEnd(self, reqId, start, end):
        q.put(reqId)
        p = 0
        for i in range(len(self.barData)):
            p += self.barData[i]
        p = p/len(self.barData)
        self.listP.append(round(p, 3))
        self.barData = []
        q.task_done()
        return super().historicalDataEnd(reqId, start, end)
    def fetchPrice(self, reqId, symbolList, secTypeList, exchangeList):
        self.Qing = True
        contract = Contract()
        for i in range(len(symbolList)):
            contract.symbol = symbolList[i]
            contract.secType = secTypeList[i]
            contract.exchange = exchangeList[i]
            contract.currency = "USD"
            self.reqHistoricalData(reqId*100 + i, contract, "", "30 S", "30 secs", "ASK", 0, 1, False, [])
            time.sleep(0.1)
            q.join()
        print("Finished Fetch, Request ID: ", reqId)
        self.Qing = False
        return
    def reqScannerSubscription(self, reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions):
        self.Qing = True
        return super().reqScannerSubscription(reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        q.put(reqId)

        self.listT.append(contractDetails.contract.symbol)
        self.listE.append(contractDetails.contract.exchange)
        self.listS.append(contractDetails.contract.secType)
        return super().scannerData(reqId, rank, contractDetails, distance, benchmark, projection, legsStr)
    def scannerDataEnd(self, reqId):
        self.cancelScannerSubscription(reqId)
        for i in range(len(self.listT)):
            q.task_done()
        print("Finished Scan, Request ID: ", reqId)
        self.Qing = False
        return super().scannerDataEnd(reqId)
    def write(self):
        with open("List.txt", "w") as f:
            for i in range(len(self.listT)):
                print("-Symbol:", self.listT[i], "-Type:", self.listS[i], "-Exchange path:", self.listE[i], 
                "-Price USD:", self.listP[i], file=f)
        f.close()
def webSocketThread(app: Screener):
        webSocketThread = threading.Thread(target=app.run, daemon=True)
        webSocketThread.start()
        return
def stkScan(assetType, assetLoc, scanCode, rows, pbottom, ptop):
        scanSub = ScannerSubscription()
        print("Searching...")

        scanSub.numberOfRows = rows
        scanSub.abovePrice = pbottom
        scanSub.belowPrice = ptop
        scanSub.marketCapBelow = 1_000_000_000
        scanSub.instrument = assetType
        scanSub.locationCode = assetLoc
        scanSub.scanCode = scanCode

        return scanSub