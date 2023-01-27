#ifndef multi_client_h
#define multi_client_h

#include "serv_socket.h"
#include <string>


namespace multic {
    class MultiClient: public sock::ServSocket {
        public:
            MultiClient(const char* address, int port): ServSocket(address, port) {};

        protected:
            virtual void onClientConnect(int clientSock);
            virtual void onClientDisconnect(int clientSock);
            virtual void onMsgRecv(int clientSock, const char* msg, int len);
    };
};

#endif // multi_client_h