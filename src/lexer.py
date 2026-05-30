# import shlex

# def attr_tokenizer(tokens:list[dict]):
#     for i in tokens:
#         if "attribute" in i.keys():
#             if i["attribute"] != "" and isinstance(i["attribute"], str):
#                 attributes = shlex.split(i["attribute"], posix = False)
#                 i["attribute"] = {}
#                 for j in attributes:
#                     key_value = j.split("=")
#                     i["attribute"][key_value[0]] = key_value[1].strip() if len(key_value) == 2 else ""
#     return tokens


import re

def attr_tokenizer(tokens: list[dict]):
    # This regex looks for an attribute name, an optional equals sign, 
    # and then grabs the value (whether it's in double quotes, single quotes, or no quotes)
    pattern = re.compile(r'([a-zA-Z0-9_:-]+)(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+))?')
    
    for i in tokens:

        if i.get("value", "").upper() in ["!DOCTYPE", "!--"]:
            continue

        if "attribute" in i and isinstance(i["attribute"], str) and i["attribute"].strip():
            attr_dict = {}
            
            # findall returns a list of tuples
            matches = pattern.findall(i["attribute"])
            
            for key, value in matches:
                # Assign the value if it exists, otherwise assign an empty string
                attr_dict[key] = value.strip().strip('"') if value else ""
                
            i["attribute"] = attr_dict
            
    return tokens










def lexer(body : str):
    length = len(body)
    i = 0
    node_list = []
    id = 0
    self_closing_tags = ["area",
                        "base",
                        "br",
                        "col",
                        "embed",
                        "hr",
                        "img",
                        "input",
                        "link",
                        "meta",
                        "param",
                        "source",
                        "track",
                        "wbr",
                        "command",
                        "keygen",
                        "menuitem",
                        "frame" ]

    while i < length:
        
        # 1. COMMENT
        if body[i:i+4] == "<!--":
            i+=4
            s = ""
            start = i
            while i < length and body[i:i+3] != "-->":
                s += body[i]
                i += 1
                
            i += 3  # Skip the closing "-->"
            
            node_list.append({
                "type": "comment",
                "value": s,
                "start": start,
                "end": i
            })

        # 2. CLOSE TAG
        elif body[i:i+2] == "</":
            start = i
            i += 2
            s = ""
            
            while i < length and body[i] != ">":
                s += body[i]
                i += 1
                
            i += 1  # Skip the closing ">"
            
            node_list.append({
                "type": "close_tag",
                "value": s,
                "start": start,
                "end": i,
                "id" : id
            })
            id = id + 1

        # 3. OPEN TAG
        elif body[i] == "<":
            start = i
            i += 1
            s = ""
            
            while i < length and body[i] != ">":
                s += body[i]
                i += 1
                
            i += 1 
            split_div = s.split(" ", 1)
            isvoid = True if split_div[0].strip() in self_closing_tags else False
            
            node_list.append({
                "type": "open_tag",
                "value": split_div[0],
                "attribute": split_div[1] if len(split_div) == 2 else "",
                "start": start,
                "end": i,
                "id" : id,
                "isvoid" : isvoid
            })
            id = id + 1

        # 4. TEXT
        else:
            start = i
            s = ""
            
        
            while i < length and body[i] != "<":
                s += body[i]
                i += 1
            
            
            if s.strip(): 
                node_list.append({
                    "type": "text",
                    "value": s,
                    "start": start,
                    "end": i
                })
    return node_list