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
	// this will be changed by the \quit command (see below, bonus not in video!)
	bool running = true;

	while (running) {
		// Make a copy of the master file descriptor set, this is SUPER important because
		// the call to select() is _DESTRUCTIVE_. The copy only contains the sockets that
		// are accepting inbound connection requests OR messages. 

		// E.g. You have a server and it's master file descriptor set contains 5 items;
		// the listening socket and four clients. When you pass this set into select(), 
		// only the sockets that are interacting with the server are returned. Let's say
		// only one client is sending a message at that time. The contents of 'copy' will
		// be one socket. You will have LOST all the other sockets.

		// SO MAKE A COPY OF THE MASTER LIST TO PASS INTO select() !!!

		fd_set masterCopy = servMaster;

		// See who's talking to us
		int currSocket = select(0, &masterCopy, nullptr, nullptr, nullptr);

		// Loop through all the current connections / potential connect
		for (int i = 0; i < currSocket; i++) {
			// Makes things easy for us doing this assignment
			SOCKET sock = masterCopy.fd_array[i];

			// Is it an inbound communication?
			if (sock == servSocket) {
				// Accept a new connection
                SOCKADDR_IN clientInfo = {0};
                int addrSz = sizeof(clientInfo);
				SOCKET client = accept(servSocket, (sockaddr*)&clientInfo, &addrSz);

				// Add the new connection to the list of connected clients
				FD_SET(client, &servMaster);

				onClientConnect(clientInfo);
			} else { // It's an inbound message
				char buf[4096];
				ZeroMemory(buf, 4096);

				// Receive message
				int bytesIn = recv(sock, buf, 4096, 0);
				if (bytesIn <= 0) {
					// Drop the client
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
};

void sock::ServSocket::fromClientbroadcast(int clientSock, const char* msg, int len) {
    for (int i = 0; i < servMaster.fd_count; i++) {
        SOCKET outSock = servMaster.fd_array[i];

        if (outSock != servSocket && outSock != clientSock) {
            toClientBroadcast(outSock, msg, len);
        };
    };
};

void sock::ServSocket::onClientConnect(SOCKADDR_IN clientInfo) {
    std::cout << "Connection from: " << inet_ntoa(clientInfo.sin_addr) <<"\r\n";
};

void sock::ServSocket::onClientDisconnect(int clientSock) {

};

void sock::ServSocket::onMsgRecv(int clientSock, const char* msg, int len) {

};
