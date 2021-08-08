from ScreenerClass import *

def main():
    app = Screener()

    contract = Contract()
    contract.symbol = "BNGO"
    contract.secType = "STK"
    contract.exchange = "BATS"
    contract.currency = "USD"

    time.sleep(1)

    app.reqHistoricalData(1, contract, queryTime, "1 D", "1 hour", "ASK", 0, 1, False, [])
    q.put(1)
    app.run()

    q.join()
    app.disconnect()

if __name__ == "__main__":
    main()