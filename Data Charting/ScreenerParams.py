from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import time

class Params(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def scannerParameters(self, xml: str):
        super().scannerParameters(xml)
        open('scanner_params.xml', 'w').write(xml)
        print("ScannerParameters received.")

def main():
    app = Params()

    app.connect(host = "127.0.0.1", port = 7497, clientId = 333)
    time.sleep(5)

    app.reqScannerParameters()
    app.run()

if __name__ == "__main__":
    main()
