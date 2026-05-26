import dns.resolver

def resolve_dns(domain_name : str):
    result = dns.resolver.resolve(domain_name, 'A')
    addr = []
    for ip in result:
        addr.append(ip.to_text())
    return addr