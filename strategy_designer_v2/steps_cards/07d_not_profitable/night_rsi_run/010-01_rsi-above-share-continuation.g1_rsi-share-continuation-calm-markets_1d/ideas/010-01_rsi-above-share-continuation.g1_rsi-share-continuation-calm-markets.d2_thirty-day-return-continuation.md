---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day return, the higher its return over the next 14 days.
Consequence: Lean long after strong months and away from the coin after weak ones, rather than relying on the RSI share.
Why:
- F3: The book loses when its side runs against the coin's own 30-day return. Longs after a negative 30-day return averaged -0.00066 a day (n=294), and shorts after a positive 30-day return averaged -0.00034 (n=319). Positions agreeing with the 30-day return earned more: longs after an up month +0.00269 (n=998), shorts after a down month +0.00058 (n=773).
- F4: The gain is graded by the 30-day return. Long days in the highest 30-day-return tercile averaged +0.00447 a day, against +0.00052 in the lowest. Short days in the highest tercile lost -0.00069 while the coin rose +0.00367 a day, against +0.00064 for shorts in the lowest tercile.
- F6: The forecast carries no 14-day information on its own. The pooled slope t was 0.0035 on 191 independent cases.
