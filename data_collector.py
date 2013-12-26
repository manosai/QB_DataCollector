import urllib3


http = urllib3.PoolManager()
r = http.request('GET', 'http://www.pro-football-reference.com/players/B/BreeDr00/touchdowns/passing/2013/')
print r.data