from os import write
from ScreenerClass import *

def main():
    app = Screener()

    app.connect("127.0.0.1", 7497, 333)
    return

if __name__ == "__main__":
    main()