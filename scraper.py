import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import time

def proccess_physical_attributes(physical_attributes):
    attributeList = []
    #Get all of the separate top-level tags
    for attribute in physical_attributes:
        attributeList.append(''.join(attribute.findAll(text=True)))
    return attributeList

#Process the title
def process_title_text(title_text):
	return title_text.contents[0]

#Process the body of the listing
def process_body_text(body_text):
	return body_text.contents[0][1:]

#Get the town information iff it exists
def process_hometown(hometown):
	return hometown.contents[0][2:-1]

#Get the relatonship status
def process_relationship_status(relationship_attributes):
    attributeList = []
    #Get all of the separate top-level tags
    for attribute in relationship_attributes:
        attributeList.append(''.join(attribute.findAll(text=True)))
    return attributeList

################ Get the List of Links to Search #############################
def getListOfLinks():
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
		#First pass to sanitize the links
		if (len(link) > 2):
			#Way to parse out the other crap links
			if (link[1] == 'm'):
				#Add it to the list
				linksToSearch.append(link)
	return linksToSearch



def scrape_link(linksToSearch):
	this_url = 'https://cnj.craigslist.org/' + linksToSearch[1]
	response = requests.get(this_url)

	soup = bs4(response.text, 'html.parser')

	#print soup.prettify(encoding='utf-8')
	print this_url

	### Get the information in the tags ###
	postBody = soup.find("section", {"id": "postingbody"})
	title    = soup.find("span", {"id": "titletextonly"})
	imageLink = soup.find("meta", {"property": "og:image"}) #Check this for ['content'] if not null

	hometown = soup.find("small")

	physical_attributes = soup.find_all("span", {"class":"personals_attrbubble personals_physical"})
	relationship_status = soup.find_all("span", {"class":"personals_attrbubble personals_situational"})

	#Sketchy regex way to find the age, since it doesn't fall neatly in the directory structure
	agePointer = soup.text.find("age:")

	age = ""
	#Fetch the age if it is not 
	if agePointer != -1:
		age = soup.text[agePointer + len("age: "): agePointer + 7]

	################################################
	# Formatting witchcraft!	
	################################################
	#Print the title text
	print process_title_text(title)
	#Print off the age
	print age
	#Print off the body of the text
	print process_body_text(postBody)
	#Print off the hometown
	print process_hometown(hometown)
	#Print off the relationship status
	if relationship_status != None:
		print process_relationship_status(relationship_status)
	#Print off the physical attributes
	if physical_attributes != None:
		print proccess_physical_attributes(physical_attributes)

def main():
	linksToSearch = getListOfLinks()
	scrape_link(linksToSearch) #Currently just picking one off the top!

#Because python is gross
if __name__ == "__main__":
	main()