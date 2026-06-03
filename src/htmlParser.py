import socket as s


def make_dict(header : str):
    """
    Make a dictionary from the header
    """
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
    """
    Parse the body of the HTTP response based on the content length
    """
    body = ''
    while(body_length > 0):
        content = fd.recv(4096)
        read = len(content)
        body = body + content.decode('utf8')
        body_length = body_length - read

    return body


# def chunk_parser(fd:s.socket):
#     body = ''
#     content = ''
#     while('\r\n\r\n' not in content):
#         content = fd.recv(4096)
#         read = len(content)
#         body = body + content.decode('utf8')

#     return body


def chunk_parser(fd: s.socket):

    """
    Parse the body of the HTTP response based on the chunked encoding
    """

    buffer = b''
    

    while b'\r\n\r\n' not in buffer:
        content = fd.recv(4096)
        

        if not content:
            break
            

        buffer += content

    return buffer.decode('utf8', errors='ignore')


def html_parser(tokens: list):
    """
    Parse the tokens into a tree structure
    """
    stack = []
    nodes = {}
    
    # Major structural tags that should block aggressive stack unwinding
    scope_tags = ["table", "td", "tr", "th", "tbody", "thead", "body", "html"]

    for i in tokens:
        if i["type"] == "open_tag":
            tag_name = i["value"].lower().strip()
            is_void = i["isvoid"] or tag_name.startswith("!doctype")

            if not is_void:
                stack.append(i["id"])
                nodes[stack[-1]] = {
                    "node_type": "element",
                    "tag_name": tag_name,
                    "parent": stack[-2] if len(stack) > 1 else 0,
                    "child": [],
                    "closing_at": 0
                }

                if nodes[stack[-1]]["parent"] > 0:
                    nodes[stack[-2]]["child"].append(stack[-1])
            else:
                nodes[i["id"]] = {
                    "node_type": "element",
                    "tag_name": tag_name,
                    "parent": stack[-1] if stack else 0,
                    "child": [],
                    "closing_at": i["id"] 
                }
                
                if stack:
                    nodes[stack[-1]]["child"].append(i["id"])

        elif i["type"] == "text":
            nodes[i["id"]] = {
                "node_type": "raw_text",
                "parent": stack[-1] if stack else 0,
                "child": []
            }
            if stack:
                nodes[stack[-1]]["child"].append(i["id"])

        # elif i["type"] == "close_tag":
        #     close_name = i["value"].lower().strip()
            
        #     match_index = -1
        #     for idx in range(len(stack) - 1, -1, -1):
        #         target_name = nodes[stack[idx]]["tag_name"]
                
        #         if target_name == close_name:
        #             match_index = idx
        #             break
                    
        #         if target_name in scope_tags and close_name not in scope_tags:
        #             break
            
        #     if match_index != -1:
        #         nodes[stack[match_index]]["closing_at"] = i["id"]
        #         stack = stack[:match_index]

        elif i["type"] == "close_tag":
            close_name = i["value"].lower().strip()
            
            match_index = -1
            for idx in range(len(stack) - 1, -1, -1):
                target_name = nodes[stack[idx]]["tag_name"]
                
                if target_name == close_name:
                    match_index = idx
                    break
                    
                if target_name in scope_tags and close_name not in scope_tags:
                    break
            
            if match_index != -1:

                nodes[stack[match_index]]["closing_at"] = i["id"]

                for sloppy_idx in range(match_index + 1, len(stack)):
                    nodes[stack[sloppy_idx]]["closing_at"] = i["id"]
                

                stack = stack[:match_index]

    return nodes


