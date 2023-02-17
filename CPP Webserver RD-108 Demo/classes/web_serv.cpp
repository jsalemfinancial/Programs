#include "../headers/web_serv.h"

void webserv::WebServ::onMsgRecv(int clientSock, const char* msg, int len) {
    std::istringstream iss(msg);
    std::vector<std::string> parsed((std::istream_iterator<std::string>(iss)), std::istream_iterator<std::string>());

    std::cout << msg << "\r\n";

    std::ostringstream request;
    std::ostringstream content;

    std::string contentFile;
    std::string contentType;

    int errCode = 404;

    if (parsed.size() >= 3 && parsed[0] == "GET") {
		contentFile = parsed[1];

		if (contentFile.back() == '/') {
            contentFile = "/index.html";
			contentType = "text/html";
		} else if (contentFile.substr(contentFile.find('.') + 1) == "css") {
            contentType = "text/css";
        } else if (contentFile.substr(contentFile.find('.') + 1) == "mjs" || contentFile.substr(contentFile.find('.') + 1) == "js") { //Clever use of find() size to get everything after file name. Thanks Stack Exchange.
            contentType = "text/javascript";
        } else if (contentFile.substr(contentFile.find('.') + 1) == "pdf") {
            contentType = "application/pdf";
        } else if (contentFile.substr(contentFile.find('.') + 1) == "png") {
            contentType = "image/*";
        } else {
            std::cout << "File Error!\r\n";
        }
	}

    std::ifstream f(".\\front" + contentFile, std::ios::binary);
    if (f.good()) {
        content.clear();

        content << f.rdbuf();
        errCode = 200;
    }

    f.close();

    // std::cout << content;

    request << "HTTP/1.1 " << errCode << " OK\r\n";
    request << "Cache-Control: no-cache, private\r\n";
    request << "Content-Disposition: inline\r\n";
    request << "Content-Type: " << contentType << "\r\n";
    request << "Content-Length: " << content.str().size() << "\r\n";
    request << "\r\n";
    request << content.str();

    std::cout << "\n";

    toClientBroadcast(clientSock, request.str().c_str(), request.str().size() + 1);

    return;
}