import socket
from src.modules.DNSMessage import DNSMessage
import random

class Logic:
    def __init__(self):
        """ Initializes the logic """
        self.root_dns_servers = ['a.root-servers.net',
                                 'b.root-servers.net',
                                 'c.root-servers.net',
                                 'd.root-servers.net',
                                 'e.root-servers.net',
                                 'f.root-servers.net',
                                 'g.root-servers.net',
                                 'h.root-servers.net',
                                 'i.root-servers.net',
                                 'j.root-servers.net']

        self.random_root_server = self.root_dns_servers[
            random.randint(0, len(self.root_dns_servers) - 1)]

    def get_dns_info(self, data):
        """ Get DNS info """
        while True:
            query = DNSMessage()
            query.initialize_message(data)
            requested_ip = socket.gethostbyname(self.random_root_server)
            print(requested_ip)
            request = query.get_message()

            """ Send requests to the servers recursively """
            while True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.sendto(request, (requested_ip, 53))
                buffer, addr = sock.recvfrom(65535)
                sock.close()
                print(f'Received {len(buffer)} bytes from {addr}')

                response = DNSMessage()
                response.initialize_message(buffer)

                domains = response.get_domains()

                if response.answers is not None:
                    return response.get_message()

                # if len(domains) <= 0:
                    # break
                requested_ip = domains[random.randint(0, len(domains) - 1)]
                # if len(domains) == 0:
                #     requested_ip = domains[0]
                #     return response.get_message()
                # requested_ip = domains[0]
