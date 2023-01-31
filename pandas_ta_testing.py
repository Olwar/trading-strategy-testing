import pandas_ta as ta
import yfinance as yf
import pandas as pd
# import minmaxscaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime

# download ethereum data from yfinance
eth = yf.download('QQQ', period='max', interval='1d')

# convert to pandas dataframe
eth = pd.DataFrame(eth)

eth.head()

list = ["above_value", "accbands", "ad", "adosc", "adx",\
    "amat", "aobv", "apo", "aroon", "atr", "bbands", \
    "below_value", "bias", "bop", "brar", "cci", "cdl_z", \
    "cfo", "cg", "chop", "cksp", "cmf", "cmo", "coppock", \
    "cross_value", "cti", "decay", "decreasing", "dema", "dm", "donchian", \
    "ebsw", "efi", "ema", "entropy", "eom", "er", "eri", "fisher", "fwma", "ha", \
     "hl2", "hlc3", "hma", "hwc", "hwma", "increasing", "inertia", \
    "jma", "kama", "kc", "kdj", "kst", "kurtosis", "kvo", "linreg", "log_return", \
    "long_run", "macd", "mad", "massi", "mcgd", "median", "mfi", "midpoint", \
    "midprice", "mom", "natr", "nvi", "obv", "ohlc4", "pdist", "percent_return", \
    "pgo", "ppo", "psl", "pvi", "pvo", "pvol", "pvr", "pvt", "pwma", \
    "qstick", "quantile", "rma", "roc", "rsi", "rsx", "rvgi", "rvi", "short_run", \
    "sinwma", "skew", "slope", "sma", "smi", "squeeze", "squeeze_pro", "ssf", "stc", \
    "stdev", "stoch", "stochrsi", "swma", "t3", "tema", "thermo", \
    "tos_stdevall", "trima", "trix", "true_range", "tsi", "tsignals", "ttm_trend", "ui", \
    "uo", "variance", "vhf", "vidya", "vortex", "vwap", "vwma", "wcp", "willr", \
    "wma", "xsignals", "zlma", "zscore"]

best_indicators = []
print("len eth: ", len(eth))
first_date = eth.index[0]
i = 0
for item in list:
    print("indicator: ", item)
    temp = eth.copy()
    temp = eval(f"temp.ta.{item}(inplace=True)")
    temp.dropna(inplace=True)
    print(temp.head())
    print(len(temp))
    date_now = temp.index[0]
    difference_len = 1904 - len(temp)
    # compare how many days between first_date and date_now
    delta = date_now - first_date
    difference_days = delta.days
    if difference_days > 200:
        print("over 200 days gone")
        break
    if difference_days != difference_len:
        print(difference_days, difference_len)
        break
    best_indicators.append(item)
    i += 1
print("best_indicators: ", best_indicators)
for item in best_indicators:
    print("Indicator: ", item)
    temp = eval(f"eth.ta.{item}()")
    # add temp to eth
    eth = eth.join(temp, how="outer", rsuffix=f"_{item}")

print("len eth: ", len(eth))
print(eth.head())
eth.dropna(inplace=True)
print("len eth: ", len(eth))

# make all values pct_change unless they are categorical
eth = eth.pct_change()

print(eth.head())
# write to csv
eth.to_csv("QQQ_pctchange.csv")
