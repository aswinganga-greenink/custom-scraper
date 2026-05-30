from src.tcpConn import create_connection, get_http_response
from src.lexer import lexer, attr_tokenizer
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict, html_parser
import re

domain = "neverssl.com"

fd = create_connection(domain)

response = get_http_response(fd, domain)

node_list = lexer(response["body"])

updated = attr_tokenizer(node_list)
nodes = html_parser(updated)

# print(updated)

# print(nodes)

# print(updated[51])

print(updated)

# for i in node_list:
#     if i["type"] == "open_tag":
#         print(i["value"], " : ", i["id"])
#         for j in node_list:
#             if nodes[i["id"]]["closing_at"] == j["id"]:
#                 print(j["value"], " : ", j["id"])


for i in node_list:
    if i["type"] == "open_tag":
        closer_id = nodes[i["id"]]["closing_at"]
        
        if closer_id == i["id"]:
            print(i["value"], " : SELF-CLOSING")
        elif closer_id == 0:
            print(i["value"], " : UNCLOSED")
        else:
            print(i["value"], " : ", node_list[closer_id]["value"])
