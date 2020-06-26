import bs4 
import requests



resp = requests.get("https://www.nytimes.com/section/education")
soup = bs4.BeautifulSoup(resp.text,"lxml")
#print(soup)
data = soup.find("div",{"class":"css-xbztij"})
f = data.find_all("a")
#a = (f["href"])
#url = "https://www.nytimes.com"+a
news = f[1].contents[0]
print(news)
