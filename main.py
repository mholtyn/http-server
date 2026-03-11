import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 9999), reuse_port=True)
    while True:
        try:    
            client_conn, adr = server_socket.accept()
            with client_conn:
                print(f"Connection from {adr} has been established!")
                client_conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        except BaseException as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()