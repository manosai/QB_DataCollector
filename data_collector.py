import sys 
import urllib3
import os 

from bs4 import BeautifulSoup
import boto.sdb

# AWS connection to SimpleDB
def aws_connect():
	conn = boto.sdb.connect_to_region('us-east-1',\
    		aws_access_key_id=os.environ['aws_access_key_id'], \
            aws_secret_access_key=os.environ['aws_secret_access_key'])
	return conn

# get QB player html source 
def main(qb_name): 
	qb_name = qb_name.replace("_", " ") 
	base_url = 'http://www.pro-football-reference.com/players/'
	last_char = qb_name.split(" ")[1][0]
	player_url = qb_name.split(" ")[1][0:4] + qb_name.split(" ")[0][0:2] + "00/"
	url = base_url + last_char + "/" + player_url + "touchdowns/passing/2013"
	http = urllib3.PoolManager()
	r = http.request('GET', url)
	parse_html(r.data, qb_name)

# get the relevant table text 
def parse_html(html, qb_name):
	soup = BeautifulSoup(html)
	results=[]
	table = soup.find("table", {"id":"scores"})
	rows = table.findAll('tr')
	lines=[]
	for tr in rows:
		cols = tr.findAll('td')
		for td in cols: 
			text=td.text.strip("\n")
			lines.append(text)
	text_table='\n'.join(lines)
	results.append(text_table) 
	build_adjacency(results, qb_name)

# build adjacency list mapping receivers to # of touchdowns
def build_adjacency(results, qb_name): 
	receivers = {}
	counter = 0
	hit_first = False 

	results = results[0].split('\n')
	for result in results:
		counter += 1
		if (counter == 10 and hit_first is False or counter % 12 == 0 and counter > 0): 
			counter = 0 
			hit_first = True 
			# if already in the hashmap, increment the count by 1
			if result in receivers.keys():
				val = receivers[result] + 1
				receivers[result] = val
			# else - is not in the hashmap, add it 
			else:
				receivers[result] = 1

	# calculate threshold for star label
	num = len(receivers.keys())
	total_tds = 0
	for receiver in receivers.keys():
		total_tds += receivers[receiver]
	threshold = total_tds / num 

	# format this into an output list of json strings
	output_list = []
	for receiver in receivers.keys(): 
		# if above threshold, build dict with star set to true
		if (receivers[receiver] >= threshold): 
			myDict = {
				"name": receiver, 
				"touchdowns": receivers[receiver], 
				"quarterback": qb_name, 
				"type": "receiver",
				"star": "true"
			}
		else: 
			myDict = {
				"name": receiver, 
				"touchdowns": receivers[receiver], 
				"quarterback": qb_name, 
				"type": "receiver",
				"star": "false"
			}
		output_list.append(myDict)
	add_data(output_list)

# store in SimpleDB
def add_data(output_list):
	conn = aws_connect()
	qb_domain = conn.get_domain('qb_table')
	for receiver_attrs in output_list:
		qb_domain.put_attributes(receiver_attrs['name'], receiver_attrs)

if __name__ == "__main__":
	main(sys.argv[1])










