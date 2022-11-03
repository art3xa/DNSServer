import socket
import threading
from src.modules.Logic import Logic


class Router:
    def __init__(self, host, port=53):
        """Initializes the server"""
        self.addr = (host, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        self.threads = []
        self.Logic = Logic()
        self.lock = threading.Lock()
        print(f'DNS Server started on "{host}", port {port}...')

    def start(self):
        """Starts the server in the multithreaded mode"""
        while True:
            try:
                data, client_addr = self.server.recvfrom(65535)
                t = threading.Thread(target=self._serve, args=(data, client_addr))
                self.threads.append(t)
                t.start()
            except (ConnectionResetError, IndexError):
                continue
            except KeyboardInterrupt:
                print('KeyboardInterrupt')
                break

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the server"""
        self.server.close()
        for thread in self.threads:
            thread.join()
        return False

    def _serve(self, data, addr):
        """Serves the client"""
        if data:
            print(f'Get data from {addr}')
            response = self.Logic.get_dns_info(data)
            with self.lock:
                self.server.sendto(response, addr)