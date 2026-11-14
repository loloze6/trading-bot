---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.d not profitable
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close is above its close five days earlier tends to rise from Friday's close to Saturday's close; the Saturday drift is a continuation of the recent rise rather than a calendar effect on its own.
Consequence: Go long into Saturday only when the coin's last five days are up, and refuse the Saturday long after a falling week.
Why:
- F1: The Saturday edge is only there when the coin is already rising: Friday-close-to-next-close returns average 0.0095 (t 6.57, n 1002 Fridays) when the 5-day return is positive, but −0.0019 (t −1.81, n 1054) when it is negative.
- F2: The book's gain before fees comes almost entirely from uptrends: active long bars make 0.0126 per bar (t 3.90, n 492) when the 20-day return is positive, but only 0.0016 (t 0.79, n 857) when it is negative, and 64% of active bars (857 of 1349) sit in the losing regime; active down20 Fridays return −0.0005 (t −0.31, n 635).
- F3: The book misses much of the edge it targets: Fridays left flat in an up20 regime still return 0.0049 (t 3.25, n 483), while the book holds 635 down20 Fridays that earn nothing.
- F5: The forecast's size carries information mainly in an uptrend: active Friday next-bar returns rise from −0.0002 to 0.0100 to 0.0169 across forecast bins 0–5, 5–10 and 10–20 when up20, but stay between −0.0019 and 0.0010 when down20; pooled, the gross forecast buckets are 0.0039 (t 2.92, n 508), 0.0032 (t 0.94, n 278) and 0.0182 (t 2.30, n 252).
