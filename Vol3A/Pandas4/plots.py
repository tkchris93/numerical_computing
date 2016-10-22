import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## CREATE DOW_AVERAGES.PNG
dow = pd.read_csv("DJIA.csv", index_col=0)
dow.index = pd.to_datetime(dow.index)
dow.replace(".", np.nan, inplace=True)
dow.VALUE = dow.VALUE.astype(float)
filled = dow.fillna(method="ffill")

plt.plot(filled.index, filled.VALUE, lw=.1, color='k', label="Original")
plt.plot(filled.index, filled.rolling(window=300).mean(), color='r', label="Rolling")
plt.plot(filled.index, filled.ewm(span=30).mean(), color='g', label="EWMA")

plt.plot(filled.index, filled.rolling(window=365).mean(), color='r')
plt.plot(filled.index, filled.ewm(span=365).mean(), color='g')
plt.legend(loc="lower right")
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Dow Jones Industrial Average")

#plt.show()
#plt.savefig("dow_averages.png")

## CREATE MOVING.PNG
N = 10000
bias = 0.01
s = np.zeros(N)
s[1:] = np.random.uniform(low=-1, high=1, size=N-1) + bias
s = pd.Series(s, index=pd.date_range("2015-10-20", freq='H', periods=N))
s = s.cumsum()

plt.subplot(121)
s.plot(lw=.3, color='grey', label="Actual")
s.rolling(window=300).mean().plot(color='r', lw=2, label="Rolling Average")
plt.legend(loc="lower right")
plt.title("Rolling Average")

plt.subplot(122)
s.plot(lw=.3, color='grey', label="Actual")
s.ewm(span=300).mean().plot(color='r', lw=2, label="EWMA")
plt.legend(loc="lower right")
plt.title("EWMA")
#plt.savefig("moving.png")
plt.show()
