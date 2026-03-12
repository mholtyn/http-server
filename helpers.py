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


def parse_request(buf: bytes) -> tuple[str, str, str, dict[str, str]]:
    """
    Parses raw bytes from client request. 
    Returns (method, path, protocol, headers).
    headers: dict with lowercase keys (e.g. headers["user-agent"]).
    """
    data = buf.decode("utf-8", errors="replace")
    lines = data.split(CRLF)
    request_line = lines[0]
    method, path, protocol = request_line.split()

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.lower()] = v.strip()

    return method, path, protocol, headers


def build_response(method: str, path: str, headers: dict[str, str]) -> str:
    """Builds full HTTP response string from parsed request."""
    if method == "GET" and path == "/":
        return f"HTTP/1.1 200 OK{CRLF}{CRLF}Hello, world"
    if method == "GET" and path.startswith("/echo/"):
        echo_body = path[6:]
        body_bytes = echo_body.encode("utf-8")
        return (
            f"HTTP/1.1 200 OK{CRLF}"
            f"Content-Type: text/plain{CRLF}"
            f"Content-Length: {len(body_bytes)}{CRLF}{CRLF}"
            f"{echo_body}"
        )
    if method == "GET" and path == "/user-agent":
        user_agent = headers.get("user-agent", "")
        body_bytes = user_agent.encode("utf-8")
        return (
            f"HTTP/1.1 200 OK{CRLF}"
            f"Content-Type: text/plain{CRLF}"
            f"Content-Length: {len(body_bytes)}{CRLF}{CRLF}"
            f"{user_agent}"
        )
    return f"HTTP/1.1 404 Not Found{CRLF}{CRLF}Not Found"