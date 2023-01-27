#include "multi_client.h"



void multic::MultiClient::onClientConnect(int clientSock) {
    std::string initMsg = "Welcome to Localhost!\n";
    toClientBroadcast(clientSock, initMsg.c_str(), initMsg.size() + 1);
};

void multic::MultiClient::onClientDisconnect(int clientSock) {

};

void multic::MultiClient::onMsgRecv(int clientSock, const char* msg, int len) {
    fromClientbroadcast(clientSock, msg, len);
};