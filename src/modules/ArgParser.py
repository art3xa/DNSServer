import argparse


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        """ Initializes the argument parser """
        super(ArgParser, self).__init__(description='DNS Server')
        self.add_argument('-p', '--port', type=int, default=53, help='Port dns server (default 53)')
        self.add_argument('-i', '--ip', type=str, default='127.0.0.1', help='Ip address of the server (default 127.0.0.1)')
