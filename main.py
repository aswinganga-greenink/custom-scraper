from src.tcpConn import create_connection, get_http_response
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict

fd = create_connection("neverssl.com")
# print(resolve_dns("geeksforgeeks.org"))
# print(resolve_dns("wikipedia.com"))

response = get_http_response(fd, "neverssl.com")

print(response)

# str_response = response.decode('utf8')
# data = str_response.split('\r\n\r\n')
# make_dict(data[0])
# for i in data:
#     print(1)
#     print(i)

# for i in response:
#     print(i)