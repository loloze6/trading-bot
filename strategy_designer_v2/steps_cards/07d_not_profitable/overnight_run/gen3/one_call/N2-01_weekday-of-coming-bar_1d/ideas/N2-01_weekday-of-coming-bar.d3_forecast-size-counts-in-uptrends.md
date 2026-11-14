---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.d not profitable
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is in an uptrend and its forecast of Saturday excess return is large, the Saturday bar's gain grows with the size of that forecast.
Consequence: Scale the Saturday long by the forecast only when the twenty-day trend is up, and stay flat or small when it is down.
Why:
- F2: The book's gain before fees comes almost entirely from uptrends: active long bars make 0.0126 per bar (t 3.90, n 492) when the 20-day return is positive, but only 0.0016 (t 0.79, n 857) when it is negative, and 64% of active bars (857 of 1349) sit in the losing regime; active down20 Fridays return −0.0005 (t −0.31, n 635).
- F5: The forecast's size carries information mainly in an uptrend: active Friday next-bar returns rise from −0.0002 to 0.0100 to 0.0169 across forecast bins 0–5, 5–10 and 10–20 when up20, but stay between −0.0019 and 0.0010 when down20; pooled, the gross forecast buckets are 0.0039 (t 2.92, n 508), 0.0032 (t 0.94, n 278) and 0.0182 (t 2.30, n 252).
