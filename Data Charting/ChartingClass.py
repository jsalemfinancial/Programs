import imp
# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd
import datetime
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class Charter(EWrapper, EClient):
    data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close"])

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
        self.data = self.data.append({"Date": datetime.datetime.strptime(bar.date, "%Y%m%d %H:%M:%S"), "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close}, ignore_index = True)

    def historicalDataEnd(self, reqId, start, end):
        self.data.to_csv(dir_path+"\\data.csv", index=False)
        print("Done writing to csv, Id: ", reqId)
        self.disconnectClient()