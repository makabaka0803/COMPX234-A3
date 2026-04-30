import socket
import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <server-hostname> <server-port> <input-file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    input_file_path = sys.argv[3]

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        sys.exit(1)

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # TASK 1: Create a TCP/IP socket and connect it to the server.
    # Hint: socket.socket(socket.AF_INET, socket.SOCK_STREAM) creates the socket.
    # Then call sock.connect((hostname, port)) to connect.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname,port))


    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 2)
            cmd = parts[0]
            message = ""

            # TASK 2: Build the protocol message string to send to the server.
            # Format:  "NNN X key"        for READ / GET
            #          "NNN P key value"   for PUT
            # where NNN is the total message length as a zero-padded 3-digit number,
            # X is "R" for READ and "G" for GET.
            # Hint: for READ/GET, size = 6 + len(key). For PUT, size = 7 + len(key) + len(value).
            # Reject lines with invalid format or key+" "+value > 970 chars.
            if cmd == 'READ':
                key = parts[1]
                # cheeck READ's key length（6 + len(key)）
                if len(key) > 970:
                    print(f"Error: READ key {key} too long (max 970 chars)")
                    continue
                length = 6 + len(key)
                message = f'{length:03d} R {key}'
            elif cmd == 'GET':
                key = parts[1]
                # check GETs key length
                if len(key) > 970:
                    print(f"Error: GET key {key} too long (max 970 chars)")
                    continue
                length = 6 + len(key)
                message = f'{length:03d} G {key}'
            elif cmd == 'PUT':
                key = parts[1]
                value = parts[2]
                # check key+" "+value's length≤970
                if len(key) + 1 + len(value) > 970:
                    print(f"Error: PUT key+value {key} {value} too long (max 970 chars)")
                    continue
                length = 7 + len(key) + len(value)
                message = f'{length:03d} P {key} {value}'

            # TASK 3: Send the message to the server, then receive the response.
            # - Send:    sock.sendall(message.encode())
            # - Receive: first read 3 bytes to get the response size (like the server does).
            #            Then read the remaining (size - 3) bytes to get the response body.
            #send:
            sock.sendall(message.encode())
            #get response size
            size_bytes = sock.recv(3)
            response_size = int(size_bytes.decode())
            #to get response body
            body_bytes = sock.recv(response_size - 3)
            response_buffer = size_bytes + body_bytes

            response = response_buffer.decode().strip()
            print(f"{line}: {response}")

    except (socket.error, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # TASK 4: Close the socket when done (already called for you — explain why
        # finally: is the right place to do this even if an error occurs above).
        sock.close()

if __name__ == "__main__":
    main()