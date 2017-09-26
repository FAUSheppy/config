import urllib3
import socket

http = urllib3.PoolManager()
socket.setdefaulttimeout(5)
url = 'https://squarez.fauiwg.de:7001/radicale/testuser/cal.ics/'
headers = urllib3.util.make_headers(basic_auth='testuser:test')
r = http.request('GET', url, headers=headers)
f = open(test.log,'w')
f.write(r)
f.close()        
