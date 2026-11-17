---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 1 day.
Consequence: Do not short a coin on a sharp down day inside an up-month, because the next day tends to rebound.
Why:
- F1: The book's loss comes from its short side. Short bars summed a position gain of -6.64 over 4141 bars, against +6.40 over 5062 long bars, and the short side lost on every one of the six coins (from -0.40 on BTC to -2.08 on XMR). Of the short side's -6.64, -4.68 is timing and -1.95 is drift.
- F2: Over one day the forecast's strongest bearish readings are followed by a rebound, not a fall. Bars with forecast at or below -10 (a large down day inside an up-month) were followed by a mean next-day return of +0.60% over 1252 bars. Mid-range and flat forecasts were followed by about +0.06%, and the bullish forecasts of 5 to 10 by -0.09%. This bounce is what makes the shorts lose even though the 7-day slope confirms.
