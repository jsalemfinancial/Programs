import datetime
import time

def start():
    currentTime = datetime.datetime.now().time()
    timeInSeconds = currentTime.hour*3600 + currentTime.minute*60 + currentTime.second
    targetTime = datetime.datetime.strptime("15:55:30", "%H:%M:%S").time()

    while (currentTime < targetTime):
        time.sleep(10 - (timeInSeconds % 10))

        currentTime = datetime.datetime.now().time()
        print("Current Time: ", currentTime)

        timeInSeconds = currentTime.hour*3600 + currentTime.minute*60 + currentTime.second

    print("Terminated at time: ", currentTime)

if __name__ == '__main__':
    start()