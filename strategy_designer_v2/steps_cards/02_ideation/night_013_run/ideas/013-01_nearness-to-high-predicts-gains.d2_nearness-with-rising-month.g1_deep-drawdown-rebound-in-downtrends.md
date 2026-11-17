---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the farther its daily close sits below its highest close of the past 60 days, the higher its return over the next 7 days.
Consequence: In a falling month, a coin deep below its recent high is a rebound candidate to buy, and one still close to its high after a down month is one to avoid holding long.
Why:
- F2: When the 30-day return is negative, the farther the close sits below its 60-day highest close, the higher the 7-day excess return: slope -0.01426 per standard deviation, t = -2.60, n = 511. The slope is negative in 5 of 6 coins and in 6 of 8 years. The deepest quintile below the high returns +0.0220 (t = 1.47), against about -0.02 in each of the other four quintiles.
- F3: The same reversal shows against the 52-week high inside falling months: slope -0.03054, t = -4.14, n = 258. Inside rising months it is flat: -0.00770, t = -1.07, n = 300. So the plan's nearness component is wrongly signed in falling markets and carries nothing in rising ones.
- F4: Inside falling months, a deeper 30-day fall is followed by a higher 7-day excess return: slope -0.00855, t = -2.05, n = 790, strongest in BTC (t = -2.85) and in 2018 (t = -2.42).
