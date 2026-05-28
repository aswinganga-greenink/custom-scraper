from src.tcpConn import create_connection, get_http_response
from src.lexer import lexer
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict
import re

domain = "textfiles.com"

fd = create_connection(domain)
# print(resolve_dns("geeksforgeeks.org"))
# print(resolve_dns("wikipedia.com"))

response = get_http_response(fd, domain)

node_list = lexer(response["body"])

print(response["status_code"])

print(node_list)
