
import json 
import os 

from bs4 import BeautifulSoup 
import boto.sdb

# AWS connection to SimpleDB
def aws_connect():
	conn = boto.sdb.connect_to_region('us-east-1',\
    		aws_access_key_id=os.environ['aws_access_key_id'], \
            aws_secret_access_key=os.environ['aws_secret_access_key'])
	return conn

# retrieve raw HTML and parse desired table 
qb_name = "Drew Brees"
soup = BeautifulSoup(open("output.html"))
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

# build the adjacency list 
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

# build an output list of json strings
output_list = []
for receiver in receivers.keys(): 
	myDict = {
	"name": receiver, 
	"touchdowns": receivers[receiver], 
	"quarterback": qb_name, 
	"type": "receiver"
	}
	output_list.append(myDict)

# store in SimpleDB
conn = aws_connect()
qb_domain = conn.get_domain('qb_table')
for receiver_attrs in output_list:
	qb_domain.put_attributes(receiver_attrs['name'], receiver_attrs)

# sanity check for getting back the right output 
query = 'select * from `qb_table` where quarterback="%s"' % qb_name
rs = qb_domain.select(query)

output = []
for attrs in rs: 
	output.append(attrs)
print json.dumps(output)





