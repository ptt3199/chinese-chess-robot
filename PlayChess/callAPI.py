import requests
import logging
from datetime import datetime

# import http.client
# http.client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
r = requests.get('https://www.chessdb.cn/chessdb.php?action=queryall&board=rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR_w', stream=True)
# print(r.encoding)

# print(datetime.now())
# enc = r.apparent_encoding
# print(enc)
#
# print(datetime.now())
# print(r.text)
# print(datetime.now())
#
# r.encoding = enc
# print(r.text)
# print(datetime.now())
# r.raw.chunked = True
# mov = r.text[5:9]
# print(mov)
print(ord('g') - ord('a'))
