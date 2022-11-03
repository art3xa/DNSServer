"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class DNSHeader:
    def __init__(self):
        self.ID = None         # 2 bytes - 16 bits identifier
        # FLAGS
        self.QR = None         # 1 bit - 0 - query, 1 - response
        self.OPCODE = None     # 4 bits - 0 - standard query, 1 - inverse query, 2 - server status request
        self.AA = None         # 1 bit - 0 - not authoritative, 1 - authoritative
        self.TC = None         # 1 bit - 0 - not truncated, 1 - truncated
        self.RD = None         # 1 bit - 0 - recursion not desired, 1 - recursion desired
        self.RA = None         # 1 bit - 0 - recursion not available, 1 - recursion available
        self.Z = None          # 3 bits - reserved for future use - must be 000
        self.RCODE = None      # 4 bits - 0 - no error, 1 - format error, 2 - server failure, 3 - name error, 4 - not implemented, 5 - refused
        # COUNTERS
        self.QDCOUNT = None    # 2 bytes - 16 bits - number of entries in the question section
        self.ANCOUNT = None    # 2 bytes - 16 bits - number of resource records in the answer section
        self.NSCOUNT = None    # 2 bytes - 16 bits - number of name server resource records in the authority records section
        self.ARCOUNT = None    # 2 bytes - 16 bits - number of resource records in the additional_section records section

        self.next_block = 12

        self.header = None

    def extract_headers(self, data):
        self.ID = data[0:2]
        self.extract_flags(data[2:4])
        self.extract_counters(data[4:12])
        self.create_bytes_header()

    def extract_flags(self, flags):
        byte1 = self.convert_byte_to_bit(bin(ord(flags[:1])).lstrip('0b'))
        byte2 = self.convert_byte_to_bit(bin(ord(flags[1:2])).lstrip('0b'))

        self.QR = str(byte1[0])
        self.OPCODE = ''
        for bit in byte1[1:5]:
            self.OPCODE += str(bit)
        self.AA = str(byte1[5])
        self.TC = str(byte1[6])
        self.RD = str(byte1[7])
        self.RA = str(byte2[0])
        self.Z = ''
        for bit in byte2[1:4]:
            self.Z += str(bit)
        self.RCODE = ''
        for bit in byte2[4:8]:
            self.RCODE += str(bit)

    @staticmethod
    def convert_byte_to_bit(byte):
        n = len(byte)
        result = []
        for i in range(0, 8 - n):
            result.append(0)
        for i in range(0, n):
            result.append(byte[i])
        return result

    def extract_counters(self, counters):
        self.QDCOUNT = counters[0:2]
        self.ANCOUNT = counters[2:4]
        self.NSCOUNT = counters[4:6]
        self.ARCOUNT = counters[6:8]

    def convert_flags(self):
        return int(self.QR + self.OPCODE + self.AA + self.TC + self.RD, 2).to_bytes(1, byteorder='big') + \
           int(self.RA + self.Z + self.RCODE, 2).to_bytes(1, byteorder='big')

    def create_bytes_header(self):
        self.header = b''
        self.header += self.ID
        self.header += self.convert_flags()
        self.header += self.QDCOUNT
        self.header += self.ANCOUNT
        self.header += self.NSCOUNT
        self.header += self.ARCOUNT

    def get_qdcount(self):
        return ord(self.QDCOUNT[:1]) + ord(self.QDCOUNT[1:2])

    def get_ancoute(self):
        return ord(self.ANCOUNT[:1]) + ord(self.ANCOUNT[1:2])

    def get_nscount(self):
        return ord(self.NSCOUNT[:1]) + ord(self.NSCOUNT[1:2])

    def get_arcount(self):
        return ord(self.ARCOUNT[:1]) + ord(self.ARCOUNT[1:2])

    def get_header(self):
        return self.header