from ScreenerClass import *
import plotly.graph_objects as go
from ibapi.contract import Contract

def main():
    app = Screener()

    stkContract = Contract()
    stkContract.symbol = "BNGO"
    stkContract.secType = "STK"
    stkContract.exchange = "SMART"
    stkContract.currency = "USD"

    app.reqHistoricalData(1, stkContract, "", "1 M", "1 hour", "TRADES", 0, 1, False, [])
    app.run()

    print("Reading and Appending Data. . .")
    prediction = "20220203  12:00:00"
    predictionTime = datetime.datetime.strptime(prediction, "%Y%m%d %H:%M:%S")

    # df0 = pd.DataFrame({"Open": [3.10], "High": [3.80], "Low": [3.00], "Close": [3.70], "Date": [prediction]})
    # df0 = df0.to_csv(dir_path+"\\data.csv", mode="a", index=True, header= False)

    df = pd.read_csv(dir_path+"\\data.csv")
    lastTime = datetime.datetime.strptime(df["Date"].iloc[-1], "%Y%m%d %H:%M:%S")
    emptyPeriods = (predictionTime - lastTime).seconds//3600
    print(emptyPeriods)

    df0 = pd.DataFrame(columns=["Open", "High", "Low", "Close"])
    for i in range(0, emptyPeriods, 1):
        df0
    # print("Writing to chart. . .")
    # fig = go.Figure(data=[go.Candlestick(x=df['Date'],
    #     open=df['Open'],
    #     high=df['High'],
    #     low=df['Low'],
    #     close=df['Close'])])
    
    # fig.show()

if __name__ == "__main__":
    main()