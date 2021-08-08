from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.scanner import ScannerSubscription
import time
import queue
import threading
import pandas as pd 
import datetime
import collections

q = queue.Queue()
queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")

class Screener(EWrapper, EClient):
    data = collections.defaultdict(list)

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connect("127.0.0.1", 7497, 333)
        self.reqMarketDataType(3)
    def connect(self, host, port, clientId):
        super().connect(host, port, clientId)

        if self.isConnected() == True:
            print("Connected!")
        else:
            print("Not Connected!")

    def error(self, reqId, errorCode, errorString):
        if reqId == -1:
            return
        else:
            print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        super().historicalData(reqId, bar)
        self.data["open"].append(bar.open)
        self.data["high"].append(bar.high)
        self.data["low"].append(bar.low)
        self.data["close"].append(bar.close)

    def historicalDataEnd(self, reqId, start, end):
        print("Done printing data!")
        df = pd.DataFrame.from_dict(self.data)
        print(df)
        df.to_csv("C:\\Users\\josep\\Documents\\GitHub\\Programs\\data.csv", index=False)
        time.sleep(5)
        q.task_done()
        print("Done writing to cvs, Id: ", reqId)
        
    def write(self):
        with open("List.txt", "w") as f:
            print("Wrote!")
        f.close()