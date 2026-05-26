import socket as s 
from src.resolveDNS import resolve_dns



def create_connection(domain_name : str, path : str='/', port : int = 80):

    ips = resolve_dns(domain_name)

    try:
        fd = s.socket(s.AF_INET, s.SOCK_STREAM)
    except s.error:
        print("Error in creation of socket")

    

    fd.connect((ips[0], port))

    print("Created a connection with the domain!")

    request = f"GET {path} HTTP/1.1\r\nHost:{domain_name}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    fd.send(request.encode())

    response = fd.recv(4096)
    fd.close()

    return response

    
