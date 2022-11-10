def get_authority_domain(data):
    """
    This method is used to extract
    the domain name from the RDATA field of the answer
    """
    domain, offset = read_name_from_bytes(data)
    return domain, offset


def get_name_length(data):
    """ Get the length of the domain name """
    length = 0
    for byte in data:
        if byte == 0:
            break
        length += 1
    return length


def read_name_from_bytes(data):
    """ Read the domain name from the bytes """
    state = 0
    expected_length = 0
    domain_string = ''
    domain_parts = []
    x = 0
    y = 0

    for byte in data:
        if state == 1:
            if byte != 0:
                domain_string += chr(byte)
            x += 1
            if x == expected_length:
                domain_parts.append(domain_string)
                domain_string = ''
                state = 0
                x = 0
            if byte == 0:
                domain_parts.append(domain_string)
                break
        else:
            state = 1
            expected_length = byte
        y += 1
    return domain_parts, y


def get_ipv4_addr(data):
    """ Convert 4 bytes to IPv4 address """
    return f"{data[0]}.{data[1]}.{data[2]}.{data[3]}"


def create_bytes(NAME, TYPE, CLASS, TTL, RDLENGTH, RDATA):
    """ Create the bytes for the section """
    return NAME + TYPE + CLASS + TTL + RDLENGTH + RDATA


def parse_first_10_bytes(data, next_block):
    """ Parse the first 10 bytes of the section """
    length = get_name_length(data)
    next_block += length
    NAME = data[:length]
    data = data[length:]

    TYPE = data[0:2]
    CLASS = data[2:4]
    TTL = data[4:8]

    RDLENGTH = data[8:10]
    data_length = ord(RDLENGTH[0:1]) + ord(RDLENGTH[1:2])
    RDATA = data[10:10 + data_length]
    next_block += data_length
    return NAME, next_block, data, TYPE, CLASS, TTL, RDLENGTH, data_length, RDATA


def convert_byte_to_bit(byte):
    """ Convert a byte to a bit """
    n = len(byte)
    result = []
    for i in range(0, 8 - n):
        result.append(0)
    for i in range(0, n):
        result.append(byte[i])
    return result