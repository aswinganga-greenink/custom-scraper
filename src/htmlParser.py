import socket as s


def make_dict(header : str):
    header_dict = {}
    meta_dict = {}
    split_elm = header.split('\r\n')

    for i in split_elm:
        key_value_list = i.split(":", 1)
        if(len(key_value_list) == 0):
            return {"Error" : "Header data missing"}, {"Error",  "Metadata Missing"}
        

        elif(len(key_value_list) == 1):

            #isolate version, status code, status text from header and the body

            meta = key_value_list[0].split(" ")
            meta_dict["version"] = meta[0].strip()
            meta_dict["status_code"] = meta[1].strip()
            meta_dict["status_text"] = meta[2].strip()


        else:
            header_dict[key_value_list[0].strip()] = key_value_list[1].strip()


    return header_dict, meta_dict



def length_parser(fd:s.socket, body_length):
    body = ''
    while(body_length > 0):
        content = fd.recv(4096)
        read = len(content)
        body = body + content.decode('utf8')
        body_length = body_length - read

    return body


def chunk_parser(fd:s.socket):
    body = ''
    content = ''
    while('\r\n\r\n' not in content):
        content = fd.recv(4096)
        read = len(content)
        body = body + content.decode('utf8')

    return body



def html_parser(tokens : list):
    stack = []
    nodes = {}

