#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import argparse
from interruptingcow import timeout

'''
Function to return the list of all comics
'''
def ListComics(link):
	#print(link)
	page = requests.get(link)
	soup = BeautifulSoup(page.content,'html.parser')
	#print(soup.prettify())

	#This should list all the comics in the page of 8muses
	list_of_all_comics = soup.find_all(class_="c-tile t-hover")
	#print("Number of tiles in this page: " + str(len(list_of_all_comics)))
	return list_of_all_comics

'''
This function is to look out for comic title-text class
'''
def TitleHunter(class_block, file_to_write):
	try:
		comic_title = class_block.find(class_="title-text").get_text()
		comic_href = class_block["href"]
		#print(comic_title)
		#print(comic_href)
		
		# Checking for comic title 
		if comic_title == "For members only" or comic_href == None:
			# Do nothing
			print("Members only or Ad block detected")
			pass
		else:
			subcomic_link = main_link + class_block["href"]
			#print(subcomic_link)
			
			subcomic_list = ListComics(subcomic_link)
			#print("Number of sublist: " + str(len(subcomic_list)))
			if subcomic_list[0].find(class_="image-title") == None:
				print("Saving the link: " + subcomic_link)
				file_to_write.write(main_link + class_block["href"] + "\n")
				file_to_write.flush()
			else:
				for subcomic in range(0, len(subcomic_list)):
					TitleHunter(subcomic_list[subcomic], file_to_write)

			#file_to_write.write(main_link + class_block["href"] + "\n")
			# Get the href value and get inside
			# will call ListComics to get all the comics blocks
			# for number of comic blocks check for title text
			# Will use recursive programming to solve this.
			# https://stackoverflow.com/questions/479343/how-can-i-build-a-recursive-function-in-python
	except Exception as e:
		#print("Invalid comic block detected! Ignoring it...")
		#print("ERROR! : " + str(e))
		pass


if __name__ == '__main__':

	class AppURLopener(urllib.request.FancyURLopener):
	    version = "Mozilla/5.0"

	parser = argparse.ArgumentParser()
	parser.add_argument("--link", help="Link of 8muses main page", default="https://www.8muses.com")
	parser.add_argument("--directory", help="Enter the directory name you want to save in", default="8muses")
	parser.add_argument("--filename", help="Enter the name of file to save the links", default="8muses_links.txt")
	args = parser.parse_args()

	global main_link
	main_link = "https://www.8muses.com"

	# Creating directory for category
	if not os.path.exists(args.directory):
		os.makedirs(args.directory)

	global file_to_write;
	file_to_write = open(args.directory + "/" + args.filename, 'a') #opening file in append mode.

	list_of_comics = ListComics(args.link)

	for comic in range(0,len(list_of_comics)):
		#print(list_of_all_comics[comic].prettify())
		print("======================== "+ str(comic) +" ==============================")
		TitleHunter(list_of_comics[comic], file_to_write)


