#VCN - FTSE Canada All Cap Index ETF (0.16%)
#VUN - U.S. Total Market Index ETF (0.05%)
#VIU - FTSE Developed All Cap ex North America Index ETF (0.22%)
#VEE - FTSE Emerging Markets All Cap Index ETF (0.24%)
#XBB - CDN bonds (0.10%)
#BTC - 
#Cash -

#pip install yfinance plotly.express plotly tweepy kaleido pandas
import yfinance as yf
import pandas as pd

#get historical market data for TSX composite (XIC)
CDN = yf.Ticker("XIC.TO").history(period="max", interval="1wk")

#clean df
CDN_df = CDN.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                    .rename(columns={"Close": "CDN_price"})
#view
#display(CDN_df)

#get historical market data for XIC (ITOT)
US = yf.Ticker("VUN.TO").history(period="max", interval="1wk")

#clean df
US_df = US.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                .rename(columns={"Close": "US_price"})
#view
#display(US_df)

#get historical market data for VIU (XEF)
INT = yf.Ticker("XEF.TO").history(period="max", interval="1wk")

#clean df
INT_df = INT.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                    .rename(columns={"Close": "INT_price"})
#view
#display(INT_df)

#get historical market data for VEE
EME = yf.Ticker("VEE.TO").history(period="max", interval="1wk")

#clean df
EME_df = EME.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                        .rename(columns={"Close": "EME_price"})
#view
#display(EME_df)

#get historical market data for XBB
CDNbond = yf.Ticker("XBB.TO").history(period="max", interval="1wk")

#clean df
CDNbond_df = CDNbond.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                        .rename(columns={"Close": "CDNbond_price"})
#view
#display(CDNbond_df)

#get historical market data for BTC
BTC = yf.Ticker("BTC-CAD").history(period="max", interval="1wk")

#clean df
BTC_df = BTC.drop(columns=['Open','High','Low','Dividends', 'Stock Splits','Volume']) \
                .rename(columns={"Close": "BTC_price"})
#view
#display(BTC_df)

#merge dfs
price_hist = pd.concat([CDN_df, US_df, INT_df, EME_df, CDNbond_df, BTC_df], axis=1)
                       #, join="inner")
price_hist.insert(0, 'tradingDay_index', range(0, len(price_hist)))

#reindex to sequential
df = price_hist.reset_index()

price_hist

###CDNeqt - VCN

#Duplicate price column
df["12m_CDNprice"] = df['CDN_price']

#shift column 1yr worth of trading days
df['12m_CDNprice'] = df['12m_CDNprice'].shift(52)

#Calculate 12m performance
df['12m_perf_CDNeq'] = (df['CDN_price']/df['12m_CDNprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_CDNprice'])

###USeqt - VUN

#Duplicate price column
df["12m_USprice"] = df['US_price']

#shift column 1yr worth of trading days
df['12m_USprice'] = df['12m_USprice'].shift(52)

#Calculate 12m performance
df['12m_perf_USeq'] = (df['US_price']/df['12m_USprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_USprice'])

###INt dev eqt - VIU

#Duplicate price column
df["12m_INTprice"] = df['INT_price']

#shift column 1yr worth of trading days
df['12m_INTprice'] = df['12m_INTprice'].shift(52)

#Calculate 12m performance
df['12m_perf_INTeq'] = (df['INT_price']/df['12m_INTprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_INTprice'])

###Eme eqt - VEE

#Duplicate price column
df["12m_EMEprice"] = df['EME_price']

#shift column 1yr worth of trading days
df['12m_EMEprice'] = df['12m_EMEprice'].shift(52)

#Calculate 12m performance
df['12m_perf_EMEeq'] = (df['EME_price']/df['12m_EMEprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_EMEprice'])

###CDNbond - VEE

#Duplicate price column
df["12m_CDNbondprice"] = df['CDNbond_price']

#shift column 1yr worth of trading days
df['12m_CDNbondprice'] = df['12m_CDNbondprice'].shift(52)

#Calculate 12m performance
df['12m_perf_CDNbond'] = (df['CDNbond_price']/df['12m_CDNbondprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_CDNbondprice'])

###BTC-CAD

#Duplicate price column
df["12m_BTCprice"] = df['BTC_price']

#shift column 1yr worth of trading days
df['12m_BTCprice'] = df['12m_BTCprice'].shift(52)

#Calculate 12m performance
df['12m_perf_BTC'] = (df['BTC_price']/df['12m_BTCprice']-1)*100

#Drop 12price column
df = df.drop(columns=['12m_BTCprice'])

df

import plotly.express as px

fig = px.line(df, x="Date", y=['12m_perf_CDNeq','12m_perf_USeq','12m_perf_INTeq',  \
                                '12m_perf_EMEeq','12m_perf_CDNbond','12m_perf_BTC'], \
              title='Trailing 12m momentum on basket of ETFs', \
              labels={"value": "12m tailing return %",
                      "variable": "ETF"}).update_traces(connectgaps=True)
fig.show()