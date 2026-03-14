import socket
import sys
import threading
from pathlib import Path

import helpers


def parse_argv() -> Path | None:
    """Parses sys.argv for --directory <path>. Returns directory for /files/ or None."""
    if len(sys.argv) >= 3 and sys.argv[1] == "--directory":
        return Path(sys.argv[2])
    return None


def handle_connection(
    client_socket: socket.socket,
    client_address: tuple,
    directory: Path | None,
) -> None:
    """Runs in a separate thread: read request, parse, build response, send, close."""
    try:
        with client_socket:
            print(f"Connection from client {client_address} has been established!")
            buf: bytes = client_socket.recv(4096)
            method, path, protocol, headers, body = helpers.parse_request(buf)
            response = helpers.build_response(method, path, headers, directory, body)
            if isinstance(response, bytes):
                client_socket.sendall(response)
            else:
                client_socket.sendall(response.encode("utf-8"))
    except Exception as error:
        print(f"Error handling {client_address}: {error}")


def main() -> None:
    print("Logs from your program will appear here!")
    directory = parse_argv()
    server_socket = socket.create_server(("localhost", 9999), reuse_port=True)
    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            thread = threading.Thread(
                target=handle_connection,
                args=(client_socket, client_addr, directory),
                daemon=True,
            )
            thread.start()
        except BaseException as error:
            print(f"Error: {error}")
            break


if __name__ == "__main__":
    main()