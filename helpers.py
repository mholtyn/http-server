import socket


CRLF = "\r\n"


# class HTTPRequest:
#     def __init__(self, data: bytes):
#         self.data = data.decode()
#         self.method, self.path, self.protocol = self.data.split(CRLF)[0].split()


# class HTTPResponse:
#     def __init__(self, status_code: int):
#         self.status_code = status_code

#     def __str__(self):
#         STATUS_CODE_PHRASES = {
#             200: "OK",
#             404: "Not Found",
#         }
#         return f"HTTP/1.1 {self.status_code} {STATUS_CODE_PHRASES[self.status_code]}{CRLF}{CRLF}"

"""
Excepted format:
HTTP/1.1 <status_code> <reason phrase> CRLF CRLF
request line CRLF +
header (empty) CRLF +
body (empty)
"""

def parse_request(buf: bytes) -> str:
    """Parses raw bytes from client request and returns response str"""
    data = buf.decode().split(CRLF)
    request_line =  data[0]
    method, path, protocol = request_line.split()

    if method == "GET" and path == "/":
        return f"HTTP/1.1 200 OK{CRLF}{CRLF}Hello, world\n"
    elif path.startswith("/echo/"):
        return f"HTTP/1.1 200 OK{CRLF}Content-Type: text\plain{CRLF}Content-Length: {len(path[6:])}{CRLF}{CRLF}{path[6:]}\n"
    else:
        return f"HTTP/1.1 400 Not Found{CRLF}{CRLF}Not Found\n"