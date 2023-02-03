#include "serv_socket.h"

// Outside method calls for ServSocket class.
int sock::ServSocket::init() {
    WSADATA wsaData;
    int initResult;

    initResult = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (initResult != 0) {
        std::cout << "WSAStartup Failed with Code: ";
        return initResult;
    };

    servSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (servSocket == INVALID_SOCKET) {
        std::cout << "Error at socket(): ";
            WSACleanup();
            return WSAGetLastError();
        }
    
    sockaddr_in hint;
    hint.sin_family = AF_INET;
    hint.sin_addr.S_un.S_addr = INADDR_ANY;
    hint.sin_port = htons(servPort);

    if (bind(servSocket, (sockaddr*)&hint, sizeof(hint)) == SOCKET_ERROR) {
        std::cout << "Error at bind: ";
        closesocket(servSocket);
        FD_CLR(servSocket, &servMaster);
        WSACleanup();

        return WSAGetLastError();
    }

    if (listen(servSocket, SOMAXCONN) == SOCKET_ERROR) {
        std::cout << "Error at socket() listen: ";
        WSACleanup();

        return WSAGetLastError();
    }

    FD_ZERO(&servMaster);
    FD_SET(servSocket, &servMaster);

    return 0;
};

int sock::ServSocket::start() {
    SOCKET client = INVALID_SOCKET;
    sockaddr_in from;
    int fromlen = sizeof(from);

    while(client == INVALID_SOCKET) {
        client = accept(servSocket, (struct sockaddr*)&from, &fromlen);
    };

    std::cout << "Connection from " << inet_ntoa(from.sin_addr) <<"\r\n";

    onClientConnect(client);
    stop();

    return 0;
};

int sock::ServSocket::stop() {

    char option = 'n';

    while (servSocket != INVALID_SOCKET) {
        std::cout <<  "Close Socket Loop on Refresh? [y/n]: ";
        std::cin >> option;
    };

    if (option == 'n') {
        start();
    } else {
        closesocket(servSocket);
        WSACleanup();
    };

    return 0;
}

void sock::ServSocket::toClientBroadcast(int clientSock, const char* msg, int len) {
    send(clientSock, msg, len, 0);
};

void sock::ServSocket::fromClientbroadcast(int clientSock, const char* msg, int len) {
    for (int i = 0; i < servMaster.fd_count; i++) {
        SOCKET outSock = servMaster.fd_array[i];

        if (outSock != servSocket && outSock != clientSock) {
            toClientBroadcast(outSock, msg, len);
        };
    };
};

void sock::ServSocket::onClientConnect(int clientSock) {
       std::cout << "Connection from " << clientSock <<"\r\n";
};

void sock::ServSocket::onClientDisconnect(int clientSock) {

};

void sock::ServSocket::onMsgRecv(int clientSock, const char* msg, int len) {

};
