import requests
import pandas
import queue
import threading

import TimeTest
import SQLDatabaseTest

class DataRequest():

    def __init__(self):
        self.url1h = "https://prices.runescape.wiki/api/v1/osrs/1h"
        self.url5m = "https://prices.runescape.wiki/api/v1/osrs/5m"
        self.urlLatest = "https://prices.runescape.wiki/api/v1/osrs/latest"

        self.headers = {
            'User-Agent': 'Name_of_Request',
            'From': 'yourcontactemail@gmail.com',
        }

    def sendReq(self):
       response = requests.get(self.urlLatest, headers=self.headers) #Defaults to latest prices.

       return response

if __name__ == "__main__":

    manager = SQLDatabaseTest.Manage(
        input("Host: "),
        input("User: "),
        input("Password: ")
    )

    print("\n")

    manager.showDatabases()

    OSRSReq = DataRequest()