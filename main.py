import socket
import helpers


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
                response = helpers.parse_request(buf)
                # send response back to the client
                client_conn.sendall(response.encode())

        except BaseException as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()