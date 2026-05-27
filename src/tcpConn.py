import socket as s 
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict



def create_connection(domain_name : str, port : int = 80):

    ips = resolve_dns(domain_name)

    try:
        fd = s.socket(s.AF_INET, s.SOCK_STREAM)
    except s.error:
        print("Error in creation of socket")

    

    fd.connect((ips[0], port))

    print("Created a connection with the domain!")
    return fd

    # request = f"GET {path} HTTP/1.1\r\nHost:{domain_name}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    # fd.send(request.encode())

    # #get first few bits of response
    # response = fd.recv(1024)
    # str_response = response.decode('utf8')
    # data = str_response.split('\r\n\r\n')

    # #make a header dictionary
    # header, http_response = make_dict(data[0])

    # body_len = int(header['Content-Length'])
    # body = ''

    # if(len(data) == 2):
    #     body = body + data[1]
    #     body_len = body_len - len(data[1])

    # while(body_len > 0):
    #     content = fd.recv(4096)
    #     read = len(content)
    #     body = body + content.decode('utf8')
    #     body_len = body_len - read

    # http_response["header"] = header
    # http_response["body"] = body


    # return http_response


def get_http_response(fd : s.socket, domain_name : str, path : str = '/'):
    request = f"GET {path} HTTP/1.1\r\nHost:{domain_name}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
    fd.send(request.encode())

    #get first few bits of response
    response = fd.recv(1024)
    str_response = response.decode('utf8')
    data = str_response.split('\r\n\r\n')

    #make a header dictionary
    header, http_response = make_dict(data[0])

    body_len = int(header['Content-Length'])
    body = ''

    if(len(data) == 2):
        body = body + data[1]
        body_len = body_len - len(data[1])

    while(body_len > 0):
        content = fd.recv(4096)
        read = len(content)
        body = body + content.decode('utf8')
        body_len = body_len - read

    http_response["header"] = header
    http_response["body"] = body



    fd.close()

    return http_response
    
