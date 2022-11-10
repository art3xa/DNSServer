from src.modules.helpers import get_name_length, create_bytes, parse_first_10_bytes
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


class DNSAuthority:
    def __init__(self):
        """ Initializes the Authority section """
        self.NAME = None      # 2 bytes - 16 bits - domain name
        self.TYPE = None      # 2 bytes - 16 bits - type of the query
        self.CLASS = None     # 2 bytes - 16 bits - class of the query
        self.TTL = None       # 4 bytes - 32 bits - time to live

        self.RDLENGTH = None  # 2 bytes - 16 bits - length of the RDATA
        self.RDATA = None     # variable - RDATA

        self.next_block = 10

        self.authority_section = None

    def extract_authority(self, data):
        """ Extracts the authority section from the raw data"""
        self.NAME, self.next_block, data, \
        self.TYPE, self.CLASS, self.TTL, \
        self.RDLENGTH, data_length, self.RDATA \
            = parse_first_10_bytes(data, self.next_block)

        self.authority_section = create_bytes(self.NAME, self.TYPE, self.CLASS,
                                              self.TTL, self.RDLENGTH, self.RDATA)

    def get_authority_section(self):
        """ Returns the authority section """
        return self.authority_section
