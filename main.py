import socket


CRLF = "\r\n"


class HTTPRequest:
    def __init__(self, data: bytes):
        self.data = data.decode()
        self.method, self.path, self.protocol = self.data.split(CRLF)[0].split()


class HTTPResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code

    def __str__(self):
        STATUS_CODE_PHRASES = {
            200: "OK",
            404: "Not Found",
        }
        return f"HTTP/1.1 {self.status_code} {STATUS_CODE_PHRASES[self.status_code]}{CRLF}{CRLF}"


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 9999), reuse_port=True)
    while True:
        try:
            # listen for inc connections    
            client_conn, adr = server_socket.accept()
            with client_conn:
                print(f"Connection from {adr} has been established!")

                # receive data from the client and parse the HTTP req
                buf: bytearray = client_conn.recv(4096)
                req = HTTPRequest(buf)

                # make decision based  on the path of the req
                response = HTTPResponse(200) if req.path == "/" else HTTPResponse(404)
                """
                Excepted format:
                HTTP/1.1 <status_code> <reason phrase> CRLF CRLF
                request line CRLF +
                header (empty) CRLF +
                body (empty)
                """
                # send response back to the client
                client_conn.sendall(str(response).encode())

        except BaseException as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()