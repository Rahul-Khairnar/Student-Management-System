import requests
import bs4

resp = requests.get("https://www.dictionary.com/e/word-of-the-day/")
soup = bs4.BeautifulSoup(resp.text,"lxml")
data = soup.find("div",{"class":"wotd-item-headword"})
f = data.find_all("a")
for g in f:
	print(g)
	print("*" * 50)
	print("*" * 50)