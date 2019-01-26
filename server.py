#  coding: utf-8 
import socketserver
import os
from pathlib import Path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


# https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
# author:Bryan Oakley
TOP_DIR = Path(os.path.abspath("www"))
HTTP_HEAD = "HTTP/1.1"

# https://andidittrich.github.io/HttpErrorPages/HTTP400.html
# author
ERROR_PAGE_TEMPLATE = """\
<html>
    <head>
        <title>Something Went Wrong</title>
    </head>
    <body>
        <h1>Message: {}</h1>
        <p>Status Code: {}</p>
    </body>
</html>
"""


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        # https://github.com/python/cpython/blob/3.7/Lib/http/server.py
        try:
            self.data = self.request.recv(1024).strip()
            self.response_text = None
            request_text = self.data.decode('utf-8')
            # print ("Got a request of: %s\n" % self.data)
            # print(request_text + "\n")
            lines = request_text.splitlines()
            lineOne = lines[0].split()
            if len(lineOne) >=3:
                if lineOne[0] == "GET" 
                    if lineOne[2] == HTTP_HEAD or float(lineOne[2].split("/")[1]) <=1.1:
                        # print("1\n")
                        response= self._handle_request(lines)
                else:
                    # print("12\n")
                    response= self._handle_error(405)
            else:
                # print("13\n")
                response = self._handle_error(404)
        except Exception as e:
            # print(e)
            # print("14\n")
            response = self._handle_error(404)

        # print(response)
        self.request.sendall(bytearray(response,'utf-8'))


    def _handle_request(self, lines):
        original_path = lines[0].split()[1]
        file_path = os.path.abspath(str(TOP_DIR) + lines[0].split()[1])
        if os.path.isdir(file_path):
            if original_path[-1] == "/":
                file_path += "/index.html"
                if os.path.isfile(file_path) and (TOP_DIR in Path(file_path).parents or str(TOP_DIR) == file_path):
                    # https://stackoverflow.com/questions/3812849/how-to-check-whether-a-directory-is-a-sub-directory-of-another-directory
                    # author: jme
                    return self._200_response(file_path, "html")
                else:
                    return self._handle_error(404)
            else:
                file_path += "/index.html"
                if os.path.isfile(file_path) and (TOP_DIR in Path(file_path).parents or str(TOP_DIR) == file_path):
                    return self._redirect(file_path, original_path)
                else:
                    return self._handle_error(404)

        elif os.path.isfile(file_path):
            if TOP_DIR in Path(file_path).parents:
                if str(file_path).endswith(".css"):
                    return self._200_response(file_path, "css")
                elif str(file_path).endswith(".html"):
                    return self._200_response(file_path, "html")
                else:
                    return self._handle_error(404)
            else:
                return self._handle_error(404)
        else:
            return self._handle_error(404)

    def _handle_error(self, status):
        if status == 404:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n"
            response += ERROR_PAGE_TEMPLATE.format("404 Not Found", 404)+ "\r\n\r\n"
        elif status == 405:
            response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n"
            response += ERROR_PAGE_TEMPLATE.format("405 Method Not Allowed", 405)+ "\r\n\r\n"
        return response

    def _redirect(self, file_path, original_path):
        response = "HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html" + "\r\n"
        response += "Location : http://127.0.0.1:" + str(PORT) + original_path+ "/\r\n\r\n"
        return response

    def _200_response(self, file_path, suffix):
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/" + suffix + "\r\n\r\n"
        # print(file_path)
        f = open(file_path, "r")
        contents =f.read()
        response += contents + "\r\n"
        return response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()