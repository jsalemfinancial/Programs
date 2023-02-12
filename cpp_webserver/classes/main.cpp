#include "../headers/web_serv.h"



int main() {
    webserv::WebServ webServer("127.0.0.1", 27015);
    if (webServer.init() != 0) {
        return 1;
    }

    webServer.start();

    system("pause");
    return 0;
}