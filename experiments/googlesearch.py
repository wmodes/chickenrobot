import urllib
import requests
from bs4 import BeautifulSoup

query = "hackernoon How To Scrape Google With Python"
query = urllib.parse.quote_plus(query)
URL = f"https://google.com/search?q={query}"

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

headers = {"user-agent" : MOBILE_USER_AGENT}
resp = requests.get(URL, headers=headers)

if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")

results = []
for div in soup.select('div:has(> a):has(> h3)'):
    for anchor in div.find_all('a'):
        for title in div.find_all('h3'):
            link = anchor['href']
            title = title.text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)
print(results)
