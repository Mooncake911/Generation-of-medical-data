# (I tried) Parsing (unused) doctors from russian site
# It work once because then you'll get ban

import requests
from bs4 import BeautifulSoup

doctors_list = []
r = requests.get("https://illness.docdoc.ru")
html = BeautifulSoup(r.content, 'html.parser')
el = html.find("ul", class_="library__specs-list")
for i in el.findAll("li"):
    title = str(el.find('a').get('title'))
    print(title)

