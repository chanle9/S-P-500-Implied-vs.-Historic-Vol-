# Historical volatility calculator for all S&P 500 constituents 

import pandas_datareader
import datetime
from pandas.plotting import register_matplotlib_converters
from bs4 import BeautifulSoup
from urllib.request import urlopen
from numpy import sqrt, mean, log, diff


# S&P 500 URL; Wikipedia
wiki_500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Extracts 500 constituents from wikipedia
def wiki_snp_500():

    with urlopen(wiki_500_url) as my_html:

        soup = BeautifulSoup(my_html, "html.parser")
        security_table = soup.find("table", class_="wikitable sortable")

        # Global variable for outside of function usage.
        global security_master
        security_master = security_table.find_all("tr")

    tickers_list = []

    for security in security_master:

        security_info = security.find_all("td")

        try:
            ticker = str(security_info[0].get_text())
            ticker = str(ticker)
            ticker = ticker.strip("\n")
            tickers_list.append(ticker)

        except:
            continue

    return(tickers_list)

# Converts function output to list.
ticker_list = wiki_snp_500()

# Alpha Vantage Panda reader module; closing price per each specified ticker.
def close_price(ticker):

    start_time = datetime.datetime(2010, 2, 13)
    end_time = datetime.datetime(2020, 3,13)
    register_matplotlib_converters()
    price = pandas_datareader.data.DataReader(ticker, "av-daily", start=start_time, \
                                              end=end_time, access_key=api_key)
    return price.close

# Historical Volatility; calculates the square root of sum of the variances of security price.
# S Variable for closing price
def historic_vol_cal(s):

    r = diff(log(s))
    r_mean = mean(r)
    diff_square = [(r[i] - r_mean) ** 2 for i in range(0, len(r))]
    std = sqrt(sum(diff_square) * (1.0 / (len(r) - 1)))
    vol = std * sqrt(252)

    return vol

for ticker in ticker_list:

    try:

        closing_price = close_price(ticker)
        ticker_historical_volatility = historic_vol_cal(closing_price)
        print(ticker)
        print(ticker_historical_volatility)

    except:

        print("Something didn't work")
        continue
        
