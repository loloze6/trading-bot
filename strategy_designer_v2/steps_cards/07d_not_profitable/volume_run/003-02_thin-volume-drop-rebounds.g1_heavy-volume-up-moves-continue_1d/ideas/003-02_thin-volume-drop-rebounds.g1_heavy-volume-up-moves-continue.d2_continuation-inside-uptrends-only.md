---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain, only while the coin's 20-day return is positive, the gain growing with that 20-day return.
Consequence: A heavy-volume surge inside a coin that is already falling over the past 20 days is a reason to refuse the long, because there the rise tends to be given back.
Why:
- F3: The continuation lives in coins already rising over the past 20 days and fails in falling ones. Active bars in the lowest quarter of 20-day return have a 5-day excess of −0.0115 and a held gain of −0.0021 per bar (318 bars), against +0.0215 in the top quarter (850 bars). On the 5-bar grid, cases with a positive 20-day return have an excess of 0.0238 (t 2.79, 277 cases), against 0.0087 (t 1.22, 234 cases) for a negative one.
- F4: The book's gain is spread thin and fragile across periods. Its mean gain is negative in 11 of 24 windows. The chained daily book has a deepest fall of −43.6%, which gives a Calmar of 0.0057. With one window left out, the lowest Sharpe is −0.09.
