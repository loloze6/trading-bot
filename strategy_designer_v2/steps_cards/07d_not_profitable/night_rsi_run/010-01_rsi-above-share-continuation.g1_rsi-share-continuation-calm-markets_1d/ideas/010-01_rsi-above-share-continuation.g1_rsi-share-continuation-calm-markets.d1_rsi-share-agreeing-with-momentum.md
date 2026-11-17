---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the higher the coin's return over the next 14 days. This holds when the coin's 30-day volatility of daily returns is low relative to its own history, and only while the coin's own 30-day return points the same way as the side RSI has held.
Consequence: Follow the side RSI has held in calm markets only when the past month's price move agrees with it, and give little weight to an RSI reading that the month's return contradicts.
Why:
- F2: The deepest fall lasted 418 days, starting in w2. In that stretch the book summed -0.549 while holding summed +0.594: BTC -0.512 against +0.471, and ETH -0.586 against +0.716. Across w2–w6, BTC longs lost -0.057 and ETH longs lost -0.111.
- F3: The book loses when its side runs against the coin's own 30-day return. Longs after a negative 30-day return averaged -0.00066 a day (n=294), and shorts after a positive 30-day return averaged -0.00034 (n=319). Positions agreeing with the 30-day return earned more: longs after an up month +0.00269 (n=998), shorts after a down month +0.00058 (n=773).
- F4: The gain is graded by the 30-day return. Long days in the highest 30-day-return tercile averaged +0.00447 a day, against +0.00052 in the lowest. Short days in the highest tercile lost -0.00069 while the coin rose +0.00367 a day, against +0.00064 for shorts in the lowest tercile.
- F5: Over 90 days the same split holds. Longs held while the 90-day return was negative lost -0.00171 a day (t=-1.38, n=125). Shorts held while the 90-day return was negative gave nothing (-0.00024, n=299).
- F6: The forecast carries no 14-day information on its own. The pooled slope t was 0.0035 on 191 independent cases.
