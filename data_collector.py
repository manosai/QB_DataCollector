import sys 
import urllib3

def main(qb_name): 
	qb_name = qb_name.replace("_", " ") 
	base_url = 'http://www.pro-football-reference.com/players/'
	last_char = qb_name.split(" ")[1][0]
	player_url = qb_name.split(" ")[1][1:4] + qb_name.split(" ")[0][0:2] + "00/"
	url = base_url + last_char + player_url + "touchdowns/passing/2013"
	print url 
	http = urllib3.PoolManager()
	r = http.request('GET', url)

if __name__ == "__main__":
	main(sys.argv[1])