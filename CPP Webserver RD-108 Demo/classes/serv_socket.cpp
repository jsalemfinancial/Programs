#include "../headers/serv_socket.h"

// Outside method calls for ServSocket class.
int sock::ServSocket::init() {
    WSADATA wsaData;
    int initResult;

    initResult = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (initResult != 0) {
        std::cout << "WSAStartup Failed with Code: ";
        return initResult;
    }

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
}

int sock::ServSocket::start() {
	while (true) {
		fd_set masterCopy = servMaster;
		int currSocket = select(0, &masterCopy, nullptr, nullptr, nullptr);

		for (int i = 0; i < currSocket; i++) {
			SOCKET sock = masterCopy.fd_array[i];

			if (sock == servSocket) {
                SOCKADDR_IN clientInfo = {0};
                int addrSz = sizeof(clientInfo);

				SOCKET client = accept(servSocket, (sockaddr*)&clientInfo, &addrSz);

				FD_SET(client, &servMaster);

				onClientConnect(clientInfo);
			} else {
				char buf[512];
				ZeroMemory(buf, sizeof(buf));

				int bytesIn = recv(sock, buf, sizeof(buf), 0);
				if (bytesIn <= 0) {
					onClientDisconnect(sock);

					closesocket(sock);
					FD_CLR(sock, &servMaster);
				} else {
					onMsgRecv(sock, buf, bytesIn);
				}
			}
		}
	}

	// Remove the listening socket from the master file descriptor set and close it
	// to prevent anyone else trying to connect.
	FD_CLR(servSocket, &servMaster);
	closesocket(servSocket);

	while (servMaster.fd_count > 0) {
		// Get the socket number
		SOCKET sock = servMaster.fd_array[0];

		// Remove it from the master file list and close the socket
		FD_CLR(sock, &servMaster);
		closesocket(sock);
	}

	// Cleanup winsock
	WSACleanup();
	return 0;
}

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
}

void sock::ServSocket::fromClientbroadcast(int clientSock, const char* msg, int len) {
    for (int i = 0; i < servMaster.fd_count; i++) {
        SOCKET outSock = servMaster.fd_array[i];

        if (outSock != servSocket && outSock != clientSock) {
            toClientBroadcast(outSock, msg, len);
        }
    }
}

void sock::ServSocket::onClientConnect(SOCKADDR_IN clientInfo) {
    std::cout << "Connection from: " << inet_ntoa(clientInfo.sin_addr) << "\r\n";
}

void sock::ServSocket::onClientDisconnect(int clientSock) {

}

void sock::ServSocket::onMsgRecv(int clientSock, const char* msg, int len) {

}
