from src.modules.DNSHeader import DNSHeader
from src.modules.DNSQuestion import DNSQuestion
from src.modules.DNSAnswer import DNSAnswer
from src.modules.DNSAuthority import DNSAuthority
from src.modules.DNSAdditional import DNSAdditional


"""
https://www.ietf.org/rfc/rfc1035.txt
                 Local Host                        |  Foreign
                                                   |
    +---------+               +----------+         |  +--------+
    |         | user queries  |          |queries  |  |        |
    |  User   |-------------->|          |---------|->|Foreign |
    | Program |               | Resolver |         |  |  Name  |
    |         |<--------------|          |<--------|--| Server |
    |         | user responses|          |responses|  |        |
    +---------+               +----------+         |  +--------+
                                |     A            |
                cache additions |     | references |
                                V     |            |
                              +----------+         |
                              |  cache   |         |
                              +----------+         |
"""

"""
    DNS message format

    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional_section information
    +---------------------+
"""

"""
    Header section format
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


class DNSMessage:
    def __init__(self):
        """ Initialize the DNS message """
        self.header = None
        self.questions = None
        self.answers = None
        self.authority = None
        self.additional = None

    def initialize_message(self, data):
        self.header = DNSHeader()
        self.header.extract_headers(data[:12])

        # Question section
        amount_questions = self.header.get_qdcount()
        pointer = self.init_questions(amount_questions, data)

        # Answer section
        amount_answers = self.header.get_ancoute()
        pointer = self.init_answers(amount_answers, data, pointer)

        # Authority section
        amount_authorities = self.header.get_nscount()
        pointer = self.init_authority(amount_authorities, data, pointer)

        # Addition section
        amount_additions = self.header.get_arcount()
        self.init_additions(amount_additions, data, pointer)

    def init_questions(self, n, data):
        """ Initialize the question section """
        self.questions = []
        pointer = 12
        for _ in range(n):
            question = DNSQuestion()
            question.extract_question(data[pointer:])
            pointer += question.nextblock
            self.questions.append(question)
        return pointer

    def init_answers(self, n, data, pointer):
        """ Initialize the answer section """
        if n == 0:
            return pointer
        self.answers = []
        for _ in range(n):
            answer = DNSAnswer()
            answer.extract_answer(data[pointer:])
            pointer += answer.next_block
            self.answers.append(answer)
        return pointer

    def init_authority(self, n, data, pointer):
        """ Initialize the authority section """
        if n == 0:
            return pointer
        self.authority = []
        for _ in range(n):
            name_server = DNSAuthority()
            name_server.extract_authority(data[pointer:])
            pointer += name_server.next_block
            self.authority.append(name_server)
        return pointer

    def init_additions(self, n, data, pointer):
        """ Initialize the addition section """
        if n == 0:
            return pointer
        elif n == 1:
            self.additional = []
            additional = DNSAdditional()
            additional.extract_extended_addition(data[pointer:])
            self.additional.append(additional)
        else:
            self.additional = []
            for i in range(n):
                additional = DNSAdditional()
                if i == n - 1:
                    additional.extract_extended_addition(data[pointer:])
                else:
                    additional.extract_additional(data[pointer:])
                    pointer += additional.next_block
                self.additional.append(additional)

    def get_domains(self):
        """ Returns a list of domains in the message """
        result = []
        try:
            for i in range(len(self.additional)):
                if self.additional[i].domain is not None:
                    result.append(self.additional[i].domain)
            return result
        except Exception:
            raise

    def get_message(self):
        """ Returns the message """
        message = b''
        message += self.header.get_header()

        if self.questions is not None:
            for i in range(len(self.questions)):
                message += self.questions[i].get_question()

        if self.answers is not None:
            for i in range(len(self.answers)):
                message += self.answers[i].get_answer_section()

        if self.authority is not None:
            for i in range(len(self.authority)):
                message += self.authority[i].get_authority_section()

        if self.additional is not None:
            for i in range(len(self.additional)):
                message += self.additional[i].get_additional_section()

        return message
