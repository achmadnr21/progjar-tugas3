import socket
import threading
import logging
import time
import request_count_request as request_counter

request_counter = request_counter.Counter()

logging.basicConfig(format='%(message)s', level=logging.WARNING)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(1024).decode('utf-8')
            if data.startswith("TIME") and data.endswith("\r\n"):
                request_counter.increment()
                print(f"[CLIENT]::[COUNTER] :: {request_counter.get_count()}")
                time_now = time.strftime("%H:%M:%S")
                message = f"JAM {time_now}\r\n"
                self.connection.sendall(message.encode('utf-8'))
            else:
                break
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.count_client = 0
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"[CLIENT]::CONNECT\t{self.client_address[0]}:{self.client_address[1]}")
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()
