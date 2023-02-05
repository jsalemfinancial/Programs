#include "web_serv.h"


// void webserv::WebServ::onClientConnect(SOCKADDR_IN clientInfo) {

// };

// void webserv::WebServ::onClientDisconnect(int clientSock) {

// };

void webserv::WebServ::onMsgRecv(int clientSock, const char* msg, int len) {
    std::istringstream iss(msg);
    std::vector<std::string> parsed((std::istream_iterator<std::string>(iss)), std::istream_iterator<std::string>());

    std::cout << msg << "\r\n";

    std::string content = "<h1 style='text-align: center'>404 Page Not Found!</h1>";
    std::string contentFile = "/index.html";
    std::string contentType = "html";
    std::ostringstream oss;
    int errCode = 404;

    if (parsed.size() >= 3 && parsed[0] == "GET") {
		contentFile = parsed[1];

		if (contentFile.back() == '/') {
            contentFile = "/index.html";
			contentType = "html";
		} else if (contentFile == "/styles.css") {
            contentType = "css";
        } else if (contentFile == "/script.js") {
            contentType = "js";
        } else {
            std::cout << "File Error!\r\n";
        };
	};

    std::ifstream f (".\\front" + contentFile);
    if (f.good()) {
        std::string str ((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
        content = str;   
        errCode = 200;
    };

    f.close();

	oss << "HTTP/1.1 " << errCode << " OK\r\n";
    oss << "Host: localhost\r\n";
	oss << "Cache-Control: no-cache, private\r\n";
	oss << "Content-Type: text/" << contentType << "\r\n";
	oss << "Content-Length: " << content.size() << "\r\n";
	oss << "\r\n";
	oss << content;

    toClientBroadcast(clientSock, oss.str().c_str(), oss.str().size() + 1);
};