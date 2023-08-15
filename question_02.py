from bs4 import BeautifulSoup
import pandas as pd
import requests


html_data = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm").text

soup = BeautifulSoup(html_data, "html.parser")

revenue_data = []
divs = soup.find_all("div", {"class":"col-xs-6"})

for div in divs:
    if "Tesla Quarterly Revenue" in div.text:
        for tr in div.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                date = tds[0].text
                revenue = tds[1].text.replace(',', '').replace('$', '')
                revenue_data.append({"Date": date, "Revenue": revenue})

tesla_revenue = pd.DataFrame(revenue_data)
                
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail(5))