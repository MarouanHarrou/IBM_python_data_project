import requests
from bs4 import BeautifulSoup
import pandas as pd


html_data = requests.get(" https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html").text

soup = BeautifulSoup(html_data, "html.parser")

body_gme_revenue = soup.find_all("tbody")[1]

revenue_data = []

for tr in body_gme_revenue.find_all("tr"):
    tds = tr.find_all("td")
    if len(tds) == 2:
        date = tds[0].text
        revenue = tds[1].text.replace(',', '').replace('$', '')
        revenue_data.append({"Date": date, "Revenue USD": revenue})

gme_revenue = pd.DataFrame(revenue_data)
print(gme_revenue.tail(5))