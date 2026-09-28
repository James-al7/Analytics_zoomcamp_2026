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
import matplotlib.pyplot as plt

def get_ipos() -> pd.DataFrame:
    """
    Fetch IPO data for the given year from stockanalysis.com.
    """
    url = f"https://www.iposcoop.com/ipos-recently-filed/"
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.3'
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Wrap HTML text in StringIO to avoid deprecation warning
        # "Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object."
        html_io = StringIO(response.text)
        tables = pd.read_html(html_io)

        if not tables:
            raise ValueError(f"No tables found")

        return tables[0]

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as ve:
        print(f"Data error: {ve}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

    return pd.DataFrame()

df_ipo.columns

df_ipos = (df_ipo["Expected To Trade"] == "Withdrawn")
df_ipos2 = df_ipo[df_ipos]
df_ipos3 = df_ipos2.copy()

import numpy as np

company_names = df_ipos3["Company"].fillna("")

conditions = [
    company_names.str.contains(
        r"\bTechnologies\b",
        regex=True
    ),

    company_names.str.contains(
        r"\bAcquisition Corp(?:oration)?\b|\bCorp\b",
        regex=True
    ),

    company_names.str.contains(
        r"\bInc\b|\bIncorporated\b",
        regex=True
    ),

    company_names.str.contains(
        r"\bGroup\b",
        regex=True
    ),

    company_names.str.contains(
        r"\bLtd\b|\bLimited\b",
        regex=True
    ),

    company_names.str.contains(
        r"\bHoldings\b|\bHolding\b",
        regex=True
    )
]

company_types = [
    "Technologies",
    "Acquisition Corp",
    "Inc.",
    "Group",
    "Limited",
    "Holdings"
]

df_ipos3["Company Type"] = np.select(
    conditions,
    company_types,
    default="Other"
)

df_ipos3["price_low_number"] = pd.to_numeric(
    df_ipos3["Price Low"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False),
    errors="coerce")

df_ipos3["price_high_number"] = pd.to_numeric(
    df_ipos3["Price High"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False),
    errors="coerce")

df_ipos3["Avg_price"] = ((df_ipos3["price_high_number"] + df_ipos3["price_low_number"]) / 2)
df_ipos3["Shares (millions)"] = pd.to_numeric(df_ipos3["Shares (millions)"], errors="coerce")

df_ipos3["Est $ Vol (millions)"] = pd.to_numeric(
    df_ipos3["Est $ Vol (millions)"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False),
    errors="coerce")

df_ipos3["Shares_offered_value"] = (
    df_ipos3["Shares (millions)"] * df_ipos3["Avg_price"]
).fillna(df_ipos3["Est $ Vol (millions)"])

company_group = df_ipos3.groupby(["Company Type"])
company_group_sum = company_group["Shares_offered_value"].sum()

