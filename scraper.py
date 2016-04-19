import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import time

################ Get the List of Links to Search #############################
base_url = 'https://cnj.craigslist.org/search/m4m'
rsp = requests.get(base_url)

html = bs4(rsp.text, 'html.parser')

listings = html.find_all('p', attrs={'class':'row'})

#Print out the links
linkList = []
for link in html.find_all('a'):
	linkList.append(link.get('href'))

#List of all
linksToSearch = []
for link in linkList:
	if (len(link) > 2):
		if (link[1] == 'm'):
			linksToSearch.append(link)


#################### Search through the items in the list #####################
this_url = 'https://cnj.craigslist.org/' + linksToSearch[1]

response = requests.get(this_url)

html = bs4(response.text, 'html.parser')

#print html.prettify(encoding='utf-8')
text = html.get_text()
print text.encode('utf-8').split('\n')


#Information to get:

# Hometown
	#class = postingtitletext
# Height 
	# class = personals_attrbubble personals_physical 
# Weight
# Status
# Age
# Description Text