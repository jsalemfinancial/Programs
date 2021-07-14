from os import write
from ScreenerClass import *

def main():
    app = Screener()

    app.connect("127.0.0.1", 7497, 333)

    webSocketThread(app)

    app.reqScannerSubscription(1, stkScan("STK", "STK.US.MAJOR", "TOP_PERC_GAIN", 40, 1, 12), [], [])
    app.mainQueue(1)
    time.sleep(1)
    mQ.join()
 
    app.fetchPrice(2, app.listT, app.listS, app.listE)
    app.mainQueue(2)
    time.sleep(1)
    mQ.join()

    print(app.listT)
    print(app.listS)
    print(app.listE)
    print(app.listP)

    app.write()
    return

if __name__ == "__main__":
    main()