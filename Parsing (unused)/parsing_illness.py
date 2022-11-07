# Parsing (unused) medical_data from russian site
# It's work always, but we don't know witch symptoms doctor treats

import requests
import pandas as pd
from bs4 import BeautifulSoup

symptom_list = []
for i in range(1, 68):
    r = requests.get("https://0370.ru/symptom/archives/page/%d" % i)
    html = BeautifulSoup(r.content, 'html.parser')
    for el in html.findAll("div", class_="p-2"):
        title = str(el.find("h4"))
        new_title = ''
        for j in range(4, len(title)-5):
            new_title += title[j]
        symptom_list.append(new_title)

data = pd.DataFrame({"Symptoms and diseases": symptom_list})
data.to_csv('D:\\Projects\\PyCharm_Projects\\big_data\\Tables\\medical_data.csv', index=False)
