from functools import reduce


def concat_helper(str_a, str_b):
    return str_a.strip() + str_b.strip()


def make_dict(header : str):
    header_dict = {}
    split_elm = header.split('\r\n')
    for i in split_elm:
        key_value_list = i.split(":", 1)
        if(len(key_value_list) == 0):
            return 0
        elif(len(key_value_list) == 1):
            header_dict["status"] = key_value_list[0].strip()
        else:
            header_dict[key_value_list[0].strip()] = key_value_list[1].strip()
    return header_dict



def html_parser(response : str):
    pass