import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


html_data = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response = requests.get(html_data).text

soup = BeautifulSoup(response, "html.parser")

gme_revenue = []
divs = soup.find_all("div", {"class":"col-xs-6"})

for div in divs:
    if "GameStop Quarterly Revenue" in div.text:
        for tr in div.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                date = tds[0].text
                revenue = tds[1].text.replace(',', '').replace('$', '')
                gme_revenue.append({"Date": date, "Revenue": revenue})

gme_revenue = pd.DataFrame(gme_revenue)
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])
gme_revenue
 
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data['Date'] = pd.to_datetime(gme_data['Date'])


make_graph(gme_data, gme_revenue, 'GameStop')