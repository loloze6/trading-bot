---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin's close is to its highest close of the past 90 days, the more it rises over the next 10 days beyond its normal drift.
Consequence: A trader should lean long on coins trading near their 90-day highs and refuse shorts there, since the move after them runs up.
Why:
- F3: The continuation is graded by recent strength on the coin's own bars. The top fifth of the 30-day return ends +3.2 % above 10-day drift (strength 0.17, t 3.21, 532 cases). The top fifth of nearness to the 90-day high ends +2.6 % (strength 0.14, t 3.03). The rank correlation of nearness with the 10-day excess move is 0.049 (p 0.012, 2645 cases). The grading is not monotone below the top fifth: the second fifth of the 30-day return shows -0.13, t -3.9.
- F4: The tested fade fights both the drift and this continuation. Its 106 cases have a total move of -1.01 % per case, -4.5 times the 0.22 % cost of a round trip. Its unusual move of +0.30 % (strength -0.038) is inside chance (t 0.97). The book's 187 shorts lost 3.86 % each after fees (median -2.07 %), for a Sharpe of -0.34.
- F2: Any fresh close above the previous 90-day high is followed by a 10-day excess rise of +3.4 % (strength 0.22, t 2.66, 197 non-overlapping cases). All other bars show -0.2 % (strength -0.01, t -0.76, 3354 cases). Such breaks never occur with a negative 30-day return, so the tested idea's falling-month breaks are a different, weaker situation.
