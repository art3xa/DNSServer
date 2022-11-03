from src.modules.helpers import read_name_from_bytes
"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class DNSQuestion:
    def __init__(self):
        self.QNAME = None     # Domain name
        self.QTYPE = None     # Type of the query
        self.QCLASS = None    # Class of the query

        self.nextblock = 4

        self.question_section = None

    def extract_question(self, data):
        self.QNAME, length = read_name_from_bytes(data)
        self.QTYPE = data[length: length + 2]
        self.QCLASS = data[length + 2: length + 4]
        self.nextblock += length
        self.create_bytes_question()

    def create_bytes_question(self):
        self.question_section = b''
        for part in self.QNAME:
            length = len(part)
            self.question_section += bytes([length])
            for char in part:
                self.question_section += ord(char).to_bytes(1, byteorder='big')

        self.question_section += self.QTYPE
        self.question_section += self.QCLASS

    def get_question(self):
        return self.question_section
