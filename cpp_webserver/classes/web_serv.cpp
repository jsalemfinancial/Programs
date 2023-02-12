#include "../headers/web_serv.h"

void webserv::WebServ::onMsgRecv(int clientSock, const char* msg, int len) {
    std::istringstream iss(msg);
    std::vector<std::string> parsed((std::istream_iterator<std::string>(iss)), std::istream_iterator<std::string>());

    std::cout << msg << "\r\n";

    std::string content = "<h1 style='text-align: center'>404 Page Not Found!</h1>";
    std::string contentFile = "/index.html";
    std::string contentType = "html";
    std::string request;
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
        } else {
            std::cout << "File Error!\r\n";
        }
	}

    std::ifstream f (".\\front" + contentFile);
    if (f.good()) {
        std::string str ((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
        content = str;   
        errCode = 200;
    }

    f.close();

    request += "GET / HTTP/1.1 "; request += errCode; request += " OK\r\n";
    request += "Cache-Control: no-cache, private\r\n";
    request += "Content-Disposition: inline\r\n";
    request += "Content-Type: "; request += contentType; request += "\r\n";
    request += "Content-Length: "; request += content.size(); request += "\r\n";
    request += "\r\n";
    std::cout << request;
    request += content;

    toClientBroadcast(clientSock, request.c_str(), strlen(request.c_str()) + 1);
}