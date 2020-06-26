import requests
import bs4



resp = requests.get("https://www.nytimes.com/section/education")
soup = bs4.BeautifulSoup(resp.text,"lxml")
data = soup.find("div",{"class":"css-xbztij"})
f = data.find("a")
a = (f["href"])
url = "https://www.nytimes.com"+a
resp = requests.get(url)
soup = bs4.BeautifulSoup(resp.text,"lxml")
print(soup)