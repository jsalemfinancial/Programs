#ifndef serv_socket_h
#define serv_socket_h

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <iostream>


namespace sock {
    class ServSocket {
        public:
            ServSocket(const char* address, int port): servAddress(address), servPort(port) {};

            int init();
            int start();
            int stop();

        protected:
            virtual void onClientConnect(SOCKADDR_IN clientSock);
            virtual void onClientDisconnect(int clientSock);
            virtual void onMsgRecv(int clientSock, const char* msg, int len);
            void toClientBroadcast(int clientSock, const char* msg, int len);
            void fromClientbroadcast(int clientSock, const char* msg, int len);
            
        private:
            const char* servAddress;
            int servPort;
            int servSocket;
            fd_set servMaster;
    };
};

#endif // serv_socket_h