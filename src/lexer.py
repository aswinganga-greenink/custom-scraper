def lexer(body : str):
    length = len(body)
    i = 0
    node_list = []

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
                "end": i
            })

        # 3. OPEN TAG
        elif body[i] == "<":
            start = i
            i += 1
            s = ""
            
            while i < length and body[i] != ">":
                s += body[i]
                i += 1
                
            i += 1 
            
            node_list.append({
                "type": "open_tag",
                "value": s,
                "start": start,
                "end": i
            })

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