from src.modules.helpers import get_name_length, get_ipv4_addr, create_bytes, \
    parse_first_10_bytes

"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class DNSAdditional:
    def __init__(self):
        """ Initializes the Additional section """
        self.NAME = None      # 2 bytes - 16 bits - domain name
        self.TYPE = None      # 2 bytes - 16 bits - type of the query
        self.CLASS = None     # 2 bytes - 16 bits - class of the query
        self.TTL = None       # 4 bytes - 32 bits - time to live

        self.RDLENGTH = None  # 2 bytes - 16 bits - length of the RDATA
        self.RDATA = None     # variable - RDATA

        self.next_block = 10

        self.domain = None

        self.additional_section = None

    def extract_additional(self, data):
        """ Extracts the additional section from the raw data """
        self.NAME, self.next_block, data, \
        self.TYPE, self.CLASS, self.TTL, \
        self.RDLENGTH, data_length, self.RDATA \
            = parse_first_10_bytes(data, self.next_block)

        if data_length == 4:
            self.domain = get_ipv4_addr(data[10:10 + data_length])
            print(self.domain)

        self.additional_section = create_bytes(self.NAME, self.TYPE, self.CLASS,
                                               self.TTL, self.RDLENGTH, self.RDATA)

    def extract_extended_addition(self, rawdata):
        """ Extracts the extended additional section from the raw data """
        self.additional_section = b'' + rawdata

    def get_additional_section(self):
        return self.additional_section
