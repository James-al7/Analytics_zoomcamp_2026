import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

import numpy as np

#Fin Data Sources
import yfinance as yf
import pandas_datareader as pdr

#Data viz
import plotly.graph_objs as go
import plotly.express as px

import time
from datetime import date

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Fetch the HTML content with headers
response = requests.get(url, headers=headers)
new_dataframes = pd.read_html(StringIO(response.text))

new_dataframe = new_dataframes[0]
row_col = new_dataframe.shape

#print(row_col)

sixth_col = new_dataframe.iloc[:, 5]  # Select all rows and the sixth column (index 5)

date_added = new_dataframe["Date added"]

date_added_datetime = pd.to_datetime(date_added, errors='coerce')

print(date_added_datetime.dt.year)

count_dict = {}
iter_count = 0

for item in date_added_year:

    iter_count += 1
    if item in count_dict:
        count_dict[item] += 1
    else:
        count_dict[item] = 1


# Alternate Version:
'''
count_by_year = {}

for year in date_added.dt.year.dropna():
    year = int(year)
    count_by_year[year] = count_by_year.get(year, 0) + 1
'''

sorted_by_addedcount_desc = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))

find_date = date.today()
end_date = date(year=find_date.year, month=find_date.month-1, day=find_date.day+7)
start_date = date(year=end_date.year, month=1, day=1)
print(f'Start Date is: {start_date}, End date is: {end_date}')

ticker_china = yf.Ticker("000001.SS")
spx_china = ticker_china.history(start=start_date, end=end_date)

ticker_hongkong = yf.Ticker("^HSI")
spx_hongkong = ticker_hongkong.history(start=start_date, end=end_date)

ticker_australia = yf.Ticker("^AXJO")
spx_australia = ticker_australia.history(start=start_date, end=end_date)

ticker_india = yf.Ticker("^NSEI")
spx_india = ticker_india.history(start=start_date, end=end_date)

ticker_canada = yf.Ticker("^GSPTSE")
spx_canada = ticker_canada.history(start=start_date, end=end_date)

ticker_germany = yf.Ticker("^GDAXI")
spx_germany = ticker_germany.history(start=start_date, end=end_date)

ticker_uk = yf.Ticker("^FTSE")
spx_uk = ticker_uk.history(start=start_date, end=end_date)

ticker_japan = yf.Ticker("^N225")
spx_japan = ticker_japan.history(start=start_date, end=end_date)

ticker_mexico = yf.Ticker("^MXX")
spx_mexico = ticker_mexico.history(start=start_date, end=end_date)

ticker_brazil = yf.Ticker("^BVSP")
spx_brazil = ticker_brazil.history(start=start_date, end=end_date)

ticker_usa = yf.Ticker("^GSPC")
spx_usa = ticker_usa.history(start=start_date, end=end_date)


spx_list = {"China": spx_china, "Hong Kong": spx_hongkong, "Australia": spx_australia, "India": spx_india, "Canada": spx_canada, "Germany": spx_germany, "United Kingdom": spx_uk, "Japan": spx_japan, "Mexico": spx_mexico, "Brazil": spx_brazil, "United States":spx_usa}
all_ytd_returns = {}

for country,value in spx_list.items():
    first_close = value["Close"].iloc[0]
    last_close = value["Close"].iloc[-1]
    ytd_return = (last_close/first_close - 1) * 100
    all_ytd_returns[country] = f"{float(ytd_return):.2f}%"