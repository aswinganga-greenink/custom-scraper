import dns.resolver

def resolve_dns(domain_name : str):
    """
    Resolve DNS for the given domain name
    """


    result = dns.resolver.resolve(domain_name, 'A')
    addr = []
    for ip in result:
        addr.append(ip.to_text())
    return addr