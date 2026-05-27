def make_dict(header : str):
    header_dict = {}
    meta_dict = {}
    split_elm = header.split('\r\n')

    for i in split_elm:
        key_value_list = i.split(":", 1)
        if(len(key_value_list) == 0):
            return {"Error" : "Header data missing"}, {"Error",  "Metadata Missing"}
        

        elif(len(key_value_list) == 1):
            # print(key_value_list)

            #isolate version, status code, status text from header and the body

            meta = key_value_list[0].split(" ")
            meta_dict["version"] = meta[0].strip()
            meta_dict["status_code"] = meta[1].strip()
            meta_dict["status_text"] = meta[2].strip()


        else:
            header_dict[key_value_list[0].strip()] = key_value_list[1].strip()


    return header_dict, meta_dict



def html_parser(response : str):
    pass