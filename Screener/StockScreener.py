from ScreenerClass import *

def main():
    app = Screener()

    stkContract = Contract()
    stkContract.symbol = "BNGO"
    stkContract.secType = "STK"
    stkContract.exchange = "SMART"
    stkContract.currency = "USD"

    time.sleep(1)

    # app.reqHistoricalData(1, stkContract, queryTime, "1 D", "1 hour", "ASK", 0, 1, False, [])
    app.reqMktData(1, stkContract, "2", False, False, [])		
    q.put(1)
    app.run()

    q.join()
    time.sleep(3)
    app.disconnect()

if __name__ == "__main__":
    main()