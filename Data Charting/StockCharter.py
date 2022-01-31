from math import ceil
from numpy import NaN
from datetime import timedelta
from ChartingClass import *
import plotly.graph_objects as go
from ibapi.contract import Contract

def main():
    queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S") #Optional lookback
    app = Charter()

    stkContract = Contract()
    stkContract.symbol = "BNGO"
    stkContract.secType = "STK"
    stkContract.exchange = "SMART"
    stkContract.currency = "USD"

    app.reqHistoricalData(1, stkContract, "", "1 M", "1 hour", "TRADES", 0, 1, False, [])
    app.run()
    
    userInput = input("Read chart (R) or place prediction (P)? \n")

    if (userInput == "R"):
        df = pd.read_csv(dir_path+"\\data.csv", index_col = 0, parse_dates=True)
        print("Writing to chart. . .")

        # See other condition for process details
        dt_all = pd.date_range(start=df.index[0],end=df.index[-1], freq="H")

        dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in df.index]

        dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]

        fig = go.Figure(data=[go.Candlestick(x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])])
        fig.update_xaxes(rangebreaks=[dict(values=dt_breaks, dvalue=60*60*1000)], rangeslider_visible=False) #dvalue specifies frequency in ms

        fig.write_html(dir_path+"\\chart.html")
        return
    elif (userInput == "P"):
        df = pd.read_csv(dir_path+"\\data.csv", index_col = 0, parse_dates=True)
        print("Reading and Appending Data. . .")
        predictionTime = datetime.datetime.strptime("2022-02-02 12:00:00", "%Y-%m-%d %H:%M:%S")
        predictionArray = [predictionTime, 3.10, 3.80, 3.00, 3.70]

        lastTime = df.index[-1]
        emptyPeriods = (predictionTime - lastTime).total_seconds()/3600
        emptyPeriods = ceil(emptyPeriods)

        df0 = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close"])
        for i in range(0, (emptyPeriods + 1)):
            if i != (emptyPeriods):
                df0 = df0.append({"Date": lastTime + timedelta(hours=i), "Open": NaN, "High": NaN, "Low": NaN, "Close": NaN}, ignore_index = True)
            else:
                print("Appending Prediction. . .")
                df0 = df0.append({"Date": predictionArray[0], "Open": predictionArray[1], "High": predictionArray[2], "Low": predictionArray[3], "Close": predictionArray[4]}, ignore_index = True)

        df0.set_index("Date", inplace=True, drop=True)
        df = df.append(df0)

        print("Done Predicting! Exporting csv")
        df.to_csv(dir_path+"\\data.csv", index=False)
        print("Writing to chart. . .")

        # Create range of values to hide breaks
        dt_all = pd.date_range(start=df.index[0],end=df.index[-emptyPeriods], freq="H") #Use to return DatetimeIndex
        #df.index[0:-emptyPeriods].strftime("%Y-%m-%d %H:%M:%S").tolist() will NOT work

        # Use List Comprehension to declare string list with dates in original set
        dt_obs = [d.strftime("%Y-%m-%d %H:%M:%S") for d in df.index]

        # define dates with missing values using List Comprehension. Turn dt_all into a date string list.
        dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d %H:%M:%S").tolist() if not d in dt_obs]

        fig = go.Figure(data=[go.Candlestick(x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'])])
        fig.update_xaxes(rangebreaks=[dict(values=dt_breaks, dvalue=60*60*1000)], rangeslider_visible=False) #dvalue specifies frequency in ms

        fig.write_html(dir_path+"\\chartPrediction.html")

        return
    else:
        print("Invalid Input. Bye!")
        return

if __name__ == "__main__":
    main()