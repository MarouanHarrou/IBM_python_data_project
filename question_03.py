import yfinance as yf

gme = yf.Ticker("GME")


gme_data = gme.history(period="max")

gme_data.reset_index(inplace=True)
print(gme_data.head(5))