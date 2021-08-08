from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.scanner import ScannerSubscription
import time
import queue
import threading
import pandas

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
        return super().historicalData(reqId, bar)
    def historicalDataEnd(self, reqId, start, end):
        return super().historicalDataEnd(reqId, start, end)
    def reqScannerSubscription(self, reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions):
        return super().reqScannerSubscription(reqId, subscription, scannerSubscriptionOptions, scannerSubscriptionFilterOptions)
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        return super().scannerData(reqId, rank, contractDetails, distance, benchmark, projection, legsStr)
    def scannerDataEnd(self, reqId):
        return super().scannerDataEnd(reqId)
    def write(self):
        with open("List.txt", "w") as f:
            print("Wrote!")
        f.close()