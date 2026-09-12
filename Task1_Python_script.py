# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import requests
import re
# Code here - Import BeautifulSoup library
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
# Code ends here

# function to get the html source text of the medium article
def get_page():
	global url
	
	# Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
	url = input("Enter url of a medium article: ").strip()
	# Code ends here
	
	# handling possible error
	if not re.match(r'https?://medium.com/',url):
		print('Please enter a valid website, or make sure it is a medium article')
		sys.exit(1)

	# The original requests.get(url) approach returned HTTP 403 for this Medium article.
	# Selenium opens the article in Chrome so BeautifulSoup can parse the loaded page.
	# The browser is closed in finally, even if loading or parsing raises an error.
	driver = webdriver.Chrome()
	try:
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, "html.parser")

		if "This website is using a security service" in soup.get_text():
			raise RuntimeError("Medium returned a block page; article was not saved.")

		return soup
	finally:
		driver.quit()

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text


def collect_text(soup):
	# text = f'url: {url}\n\n'
	# para_text = soup.find_all('p')
	# print(f"paragraphs text = \n {para_text}")
	# for para in para_text:
	# 	text += f"{para.text}\n\n"
	# return text

	# Search within the <article> element to keep the output focused on the article text.
	article = soup.find('article') # Locate the main article section.
	if article is None:
		raise RuntimeError("Article content was not found; text file was not saved.")

	paragraphs = article.find_all('p') # Collect paragraphs only within it.
	if not paragraphs:
		raise RuntimeError("No article paragraphs were found; text file was not saved.")

	text = f'url: {url}\n\n'
	for para in paragraphs:
		text += f"{para.get_text(' ', strip=True)}\n\n"
	return text

# function to save file in the current directory
def save_file(text):
	if not os.path.exists('./scraped_articles'):
		os.mkdir('./scraped_articles')
	name = url.split("/")[-1]
	print(name)
	fname = f'scraped_articles/{name}.txt'
	
	# Code here - write a file using with (2 lines)
	with open(fname, "w", encoding="utf-8") as file:
		file.write(text)
	# Code ends here

	print(f'File saved in directory {fname}')


if __name__ == '__main__':
	text = collect_text(get_page())
	save_file(text)
	# Instructions to Run this python code
	# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7