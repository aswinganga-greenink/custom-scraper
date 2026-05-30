from src.tcpConn import create_connection, get_http_response
from src.lexer import lexer, attr_tokenizer
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict, html_parser
import re

domain = "textfiles.com"

fd = create_connection(domain)

response = get_http_response(fd, domain)

node_list = lexer(response["body"])

attr_tokenizer(node_list)

print(node_list)
