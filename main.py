from src.tcpConn import create_connection
from src.resolveDNS import resolve_dns

response = create_connection("neverssl.com")
# print(resolve_dns("geeksforgeeks.org"))
# print(resolve_dns("wikipedia.com"))


print(response)

# for i in response:
#     print(i)