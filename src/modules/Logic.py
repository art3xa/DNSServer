import socket
from src.modules.DNSMessage import DNSMessage
import random
import sqlite3
import datetime


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

            """ Check if the domain is in the cache """
            name_domain, Id, TTL = query.get_name_dom()
            type = query.get_type()
            print(f'NAME DOMAIN: {name_domain}', f'ID: {Id}', f'TTL: {TTL}')

            con = sqlite3.connect('cache.db')
            cur = con.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS cache (domain, ttl, message)""")
            cur.execute("""SELECT * FROM cache WHERE domain = ?""", (name_domain,))
            res = cur.fetchone()

            if res and type == b'\x00\x01':
                print("Get from database", res)
                date_time = datetime.datetime.strptime(res[1], '%Y-%m-%d %H:%M:%S.%f')
                if date_time > datetime.datetime.now():
                    answer = res[2]
                    answer = bytearray(answer)
                    answer[:2] = Id
                    return answer
                else:
                    cur.execute("""DELETE FROM cache WHERE domain = ?""", (name_domain,))

            requested_ip = socket.gethostbyname(self.random_root_server)
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
                    message = response.get_message()

                    """ Save response to the database """
                    new_name, new_id, TTL = response.get_name_dom()
                    if TTL is not None and type == b'\x00\x01':
                        TTL = int.from_bytes(TTL, byteorder='big')
                        ttl = datetime.datetime.now() + datetime.timedelta(
                            seconds=TTL)
                        print("TTL:", ttl)
                        self.save_response(con, name_domain, message, ttl)

                    print(message)
                    return message

                requested_ip = domains[random.randint(0, len(domains) - 1)]

    @staticmethod
    def save_response(con, name_domain, message, TTL):
        """ Save response to the database """
        cur = con.cursor()
        cur.execute(f"INSERT INTO cache VALUES (?, ?, ?)", (name_domain, TTL,  message))
        con.commit()
