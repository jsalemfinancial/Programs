from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import queue
import pandas as pd
import datetime
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

q = queue.Queue()
queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")

class Screener(EWrapper, EClient):
    data = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Date"])

    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)

        self.connect("127.0.0.1", 7497, 333)
        self.checkConnection()
        self.reqMarketDataType(4)

    def checkConnection(self):
        if self.isConnected() == True:
            print("Connected!")
        else:
            print("Failed to Connect!")

    def disconnectClient(self):
        if self.isConnected() == True:
            self.disconnect()
        else:
            print("Disconnected. Bye!")
            return

    def error(self, reqId, errorCode, errorString):
        if reqId == -1:
            return
        else:
            print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        self.data = self.data.append({"Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "Date": bar.date}, ignore_index = True)

    def historicalDataEnd(self, reqId, start, end):
        print(self.data)
        print("Done printing data!")
        self.data.to_csv(dir_path+"\\data.csv", index=True)
        print("Done writing to cvs, Id: ", reqId)
        self.disconnectClient()