import socket
import time
from pathlib import Path

CRLF = "\r\n"
FILES_PREFIX = "/files/"


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


def parse_request(buf: bytes) -> tuple[str, str, str, dict[str, str], bytes]:
    """
    Parses raw bytes from client request.
    Returns (method, path, protocol, headers, body).
    headers: dict with lowercase keys (e.g. headers["user-agent"]).
    """
    data = buf.decode(encoding="utf-8", errors="replace")
    parts = data.split(CRLF + CRLF, 1)
    head = parts[0]
    body = parts[1].encode("utf-8") if len(parts) > 1 else b""
    lines = head.split(CRLF)
    request_line = lines[0]
    method, path, protocol = request_line.split()

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.lower()] = v.strip()

    return method, path, protocol, headers, body


def build_response(
    method: str,
    path: str,
    headers: dict[str, str],
    directory: Path | None = None,
    body: bytes = b"",
    should_close_connection: bool = False,
) -> str | bytes:
    """Builds full HTTP response string or bytes from parsed request."""
    connection_header = f"Connection: close{CRLF}" if should_close_connection else ""
    if method == "GET" and path == "/":
        # time.sleep(3)
        return f"HTTP/1.1 200 OK{CRLF}{connection_header}{CRLF}Hello, world"
    elif method == "GET" and path.startswith("/echo/"):
        echo_body = path[6:]
        echo_bytes = echo_body.encode("utf-8")
        return (
            f"HTTP/1.1 200 OK{CRLF}"
            f"Content-Type: text/plain{CRLF}"
            f"Content-Length: {len(echo_bytes)}{CRLF}"
            f"{connection_header}"
            f"{CRLF}"
            f"{echo_body}"
        )
    elif method == "GET" and path.startswith("/user-agent"):
        user_agent = headers.get("user-agent", "")
        body_bytes = user_agent.encode("utf-8")
        return (
            f"HTTP/1.1 200 OK{CRLF}"
            f"Content-Type: text/plain{CRLF}"
            f"Content-Length: {len(body_bytes)}{CRLF}"
            f"{connection_header}"
            f"{CRLF}"
            f"{user_agent}"
        )
    elif method == "GET" and path.startswith(FILES_PREFIX) and directory is not None:
        filename = path[len(FILES_PREFIX):].lstrip("/")
        if ".." in filename or "/" in filename:
            return (
                f"HTTP/1.1 404 Not Found{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        file_path = (directory / filename).resolve()
        try:
            file_bytes = file_path.read_bytes()
        except FileNotFoundError:
            return (
                f"HTTP/1.1 404 Not Found{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        except PermissionError:
            return (
                f"HTTP/1.1 403 Forbidden{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        except OSError:
            return (
                f"HTTP/1.1 500 Internal Server Error{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        header = (
            f"HTTP/1.1 200 OK{CRLF}"
            f"Content-Type: application/octet-stream{CRLF}"
            f"Content-Length: {len(file_bytes)}{CRLF}"
            f"{connection_header}"
            f"{CRLF}"
        )
        return header.encode("utf-8") + file_bytes
    elif method == "POST" and path.startswith(FILES_PREFIX) and directory is not None:
        filename = path[len(FILES_PREFIX):].lstrip("/")
        if ".." in filename or "/" in filename:
            return (
                f"HTTP/1.1 404 Not Found{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        file_path = (directory / filename).resolve()
        try:
            file_path.write_bytes(body)
        except OSError:
            return (
                f"HTTP/1.1 404 Not Found{CRLF}"
                f"{connection_header}"
                f"{CRLF}"
            )
        return (
            f"HTTP/1.1 201 Created{CRLF}"
            f"{connection_header}"
            f"{CRLF}"
        )
    else:
        return (
            f"HTTP/1.1 404 Not Found{CRLF}"
            f"{connection_header}"
            f"{CRLF}"
        )