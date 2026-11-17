---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close is to its 30-day high, measured in units of its 30-day daily volatility, the higher its return over the next 7 days, and the more so the higher its 7-day volume relative to its 30-day volume.
Consequence: Favour longs in coins pressing their monthly high on rising volume over those nearing it on thin trade.
Why:
- F5: Closeness to the 30-day high helps mainly when volume is also rising. Coins in the top tercile of closeness and the top tercile of 7-day volume earned +2.17% excess over 7 days (n 250), against +0.11% for the top closeness tercile with low volume (n 129) and about -1.2% for the bottom closeness tercile. This runs against the brief's worry that follow-through comes on thin volume.
- F6: Closeness to the 30-day high scaled by 30-day daily volatility predicts the 7-day excess return (slope 0.0040, t 3.10, n 1723; t 2.17 in trending bars). Raw closeness is weaker (t 1.51).
