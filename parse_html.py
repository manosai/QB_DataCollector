from bs4 import BeautifulSoup 
import json 

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
print json.dumps(receivers)



