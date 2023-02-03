#ifndef web_serv_h
#define web_serv_h

#include "serv_socket.h"
#include <string>
#include <sstream>
#include <fstream>


namespace webserv {
    class WebServ: public sock::ServSocket {
        public:
            WebServ(const char* address, int port): ServSocket(address, port) {};

        protected:
            virtual void onClientConnect(int clientSock);
            virtual void onClientDisconnect(int clientSock);
            virtual void onMsgRecv(int clientSock, const char* msg, int len);
    };
};

#endif // web_serv_h