import socket as s 
from faircrawler.resolveDNS import resolve_dns
from faircrawler.htmlParser import make_dict, length_parser, chunk_parser



def create_connection(domain_name : str, port : int = 80):
    """
    Create a TCP connection with the given domain name
    """

    ips = resolve_dns(domain_name)

    try:
        fd = s.socket(s.AF_INET, s.SOCK_STREAM)
    except s.error:
        print("Error in creation of socket")

    

    fd.connect((ips[0], port))

    print("Created a connection with the domain!")
    return fd


def get_http_response(fd : s.socket, domain_name : str, path : str = '/'):
    """
    Get the HTTP response from the given domain name
    """

    request = f"GET {path} HTTP/1.1\r\nHost:{domain_name}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    fd.send(request.encode())

    #get first few bits of response
    response = fd.recv(2048)
    str_response = response.decode('utf8')
    data = str_response.split('\r\n\r\n', 1)

    #make a header dictionary
    header, http_response = make_dict(data[0])
    body = ''

    header_keys = header.keys()

    if(len(data) == 2):
        body = body + data[1]

    if "Content-Length" in header_keys and "Transfer-Encoding" not in header_keys:
        body_len = int(header['Content-Length'])
        body_len = body_len - len(data[1])
        body = body + length_parser(fd, body_len)
    
    elif "Transfer-Encoding" in header_keys and "Content-Length" not in header_keys:
        if header["Transfer-Encoding"] == "chunked":
            if "\r\n\r\n" in body:
                pass
            else:
                body = body + chunk_parser(fd)

    else:
        body_len = int(header['Content-Length'])
        body = length_parser(fd, body_len)



    http_response["header"] = header
    http_response["body"] = body



    fd.close()

    return http_response
    
