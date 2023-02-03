#include "web_serv.h"


void webserv::WebServ::onClientConnect(int clientSock) {

    std::ifstream f (".\\front\\index.html");
    std::string output = "404 Page Not Found!";
    int outputSz = output.size() + 1;

    if (f.good()) {

    };
    std::string msg = "";

    std::ostringstream oss;
    std::string servMsg;

    oss << "HTTP/1.1 200 OK\r\n";
    oss << "Host: localhost\r\n";
    oss << "Cache-Control: no-cache, private\r\n";
    oss << "Content-Type: text/plain\r\n";
    oss << "Content-Length: 5\r\n";
    oss << "\r\n";
    oss << "Hello";

    msg = oss.str();
    toClientBroadcast(clientSock, msg.c_str(), msg.size());
};

void webserv::WebServ::onClientDisconnect(int clientSock) {

};

void webserv::WebServ::onMsgRecv(int clientSock, const char* msg, int len) {

};