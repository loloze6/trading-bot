---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close below the 200-day average is followed by further decline over the next two weeks when the 200-day average itself has been falling over the past month, and most clearly in middling volatility.
Consequence: A trader would take shorts below the long average only when that average is sloping down, and refuse them when it is rising.
Why:
- F4: Downward persistence appears only under a falling long average. Shorts held while the SMA200 was falling saw a 10-bar excess of -0.49% (t -0.82), with the mid-volatility tercile the strongest at -1.70% (t -1.65). Shorts held while the SMA200 was rising saw +0.47%.
- F6: Gains come only from periods when the coin fell, and losses from periods when it rose. 2018 earned +0.00166 gross per bar while the coin fell -0.0035, and w2, w7, w9 and w14 were also positive with the coin falling. w16 lost -0.0084 with the coin up +0.0045, and 2020 lost -0.0030 with the coin up +0.0042.
- F8: Because the forecast is standardised over its own past, the book is often short above the SMA200. The shallowest active quintile sits on average +13.3% above the average, and the book is active on 57% of bars.
