import socket
import threading

import helpers


def handle_connection(client_conn: socket.socket, client_address: tuple) -> None:
    """Runs in a separate thread: read request, parse, build response, send, close."""
    try:
        with client_conn:
            print(f"Connection from {client_address} has been established!")
            buf: bytes = client_conn.recv(4096)
            method, path, protocol, headers = helpers.parse_request(buf)
            response = helpers.build_response(method, path, headers)
            client_conn.sendall(response.encode())
    except Exception as error:
        print(f"Error handling {client_address}: {error}")


def main() -> None:
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 9999), reuse_port=True)
    while True:
        try:
            client_conn, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_connection,
                args=(client_conn, client_address),
                daemon=True,
            )
            thread.start()
        except BaseException as error:
            print(f"Error: {error}")
            break


if __name__ == "__main__":
    main()