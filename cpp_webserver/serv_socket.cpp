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
    hint.sin_port = htons(servPort);
    inet_pton(AF_INET, servAddress, &hint.sin_addr);

    int bindResult = bind(servSocket, (sockaddr* )&hint, sizeof(hint));
    if (bindResult == SOCKET_ERROR) {
        std::cout << "Error at bind: ";
        closesocket(servSocket);
        FD_CLR(servSocket, &servMaster);
        WSACleanup();

        return WSAGetLastError();
    }

    SOCKET listenResult = listen(servSocket, SOMAXCONN);
    if (listenResult == SOCKET_ERROR) {
        std::cout << "Error at socket() listen: ";
        WSACleanup();

        return WSAGetLastError();
    }

    FD_ZERO(&servMaster);
    FD_SET(servSocket, &servMaster);

    return 0;
};

int sock::ServSocket::start() {
    fd_set masterCopy = servMaster;

    int sockets = select(0, &masterCopy, nullptr, nullptr, nullptr);

    for (int i = 0; i < sockets; i++) {
        SOCKET sock = masterCopy.fd_array[i];

        if (sock == servSocket) {
            SOCKET client = accept(servSocket, nullptr, nullptr);

            FD_SET(client, &servMaster);

            onClientConnect(client);
        } else {
            char buffer[512];
            ZeroMemory(buffer, 512);

            int szIn = recv(sock, buffer, 512, 0);
            if (szIn <= 0) {

                onClientDisconnect(sock);

                closesocket(sock);
                FD_CLR(sock, &servMaster);
            } else {
                onMsgRecv(sock, buffer, szIn);
            };
        };
    };

    FD_CLR(servSocket, &servMaster);
    closesocket(servSocket);

    while (servMaster.fd_count > 0) {
        SOCKET sock = servMaster.fd_array[0];

        FD_CLR(sock, &servMaster);
        closesocket(sock);
    };

    WSACleanup();
    return 0;
};

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

};

void sock::ServSocket::onClientDisconnect(int clientSock) {

};

void sock::ServSocket::onMsgRecv(int clientSock, const char* msg, int len) {

};
