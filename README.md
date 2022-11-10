# DNSServer
DNS server that iteratively polls the servers responsible for the zone

# Usage
`python dns.py`

Or with parameters ip and port of DNS server

`python dns.py -i <ip> -p <port>`

After running the server, you can query it with the following command:

- `dig @<ip> <domain>`
- `nslookup <domain> <ip>`
- `host <domain> <ip>`

## Functionality
- Manual generation of requests and responses is used
- Simultaneous work with multiple clients
- Iterative polling of the servers responsible for the zone
- Support for multiple record types
- Caching of the answers received from the servers responsible for the zone


### Support for multiple record types
- A
- MX
- NS
- SOA
- TXT

