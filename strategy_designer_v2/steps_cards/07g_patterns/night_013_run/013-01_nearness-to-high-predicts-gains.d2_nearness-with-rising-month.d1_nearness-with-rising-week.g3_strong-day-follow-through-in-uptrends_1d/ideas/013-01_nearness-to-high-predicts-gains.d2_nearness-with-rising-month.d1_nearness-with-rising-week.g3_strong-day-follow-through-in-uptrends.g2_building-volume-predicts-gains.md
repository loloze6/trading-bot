---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day average volume relative to its 30-day average volume, the higher its return over the next 7 days.
Consequence: Lean long on coins whose trading volume has been building over the past week.
Why:
- F4: Rising recent volume predicts higher 7-day returns, the strongest pattern seen across all angles. The log of the 7-day mean volume over the 30-day mean volume has a slope of 0.028 on the 7-day excess return (t 3.47, n 1723 non-overlapping cases), t 2.73 in trending bars and t 3.34 in the later windows. It is carried mostly by XRP (t 3.09) and ZEC (t 2.58).
- F5: Closeness to the 30-day high helps mainly when volume is also rising. Coins in the top tercile of closeness and the top tercile of 7-day volume earned +2.17% excess over 7 days (n 250), against +0.11% for the top closeness tercile with low volume (n 129) and about -1.2% for the bottom closeness tercile. This runs against the brief's worry that follow-through comes on thin volume.
