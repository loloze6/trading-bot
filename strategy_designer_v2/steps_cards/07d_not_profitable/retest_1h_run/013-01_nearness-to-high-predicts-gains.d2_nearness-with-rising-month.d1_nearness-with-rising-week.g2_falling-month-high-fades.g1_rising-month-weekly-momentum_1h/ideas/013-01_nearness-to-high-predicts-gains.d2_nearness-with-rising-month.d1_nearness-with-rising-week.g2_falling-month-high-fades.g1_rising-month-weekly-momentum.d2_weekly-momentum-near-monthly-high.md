---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days, and the more so the closer its close stands to its highest close of the last 30 days.
Consequence: A rising week is worth buying mainly when it carries the coin up to its 30-day high, and much less when the coin is still far below that high.
Why:
- F5: Closeness to the 30-day high carries the gain, as the brief says. Long bars in the top quintile by distance to the 30-day high (mean 1.1% below it) earn 0.0034 per day (t 3.4). The quintile 4% below earns 0.0029 (t 4.3), the quintiles 8% and 14% below earn 0.0004 and 0.0010, and the quintile 30% below earns 0.0002.
- F3: The follow-through is not proportional to the week's rise. On the trending 168-bar grid, the two lower 7-day-return quartiles return -0.011 to +0.017 (t between -1.06 and 1.25). The two upper quartiles return 0.024 to 0.039 (t 1.86 to 2.23). On the 24-hour grid, long bars in the two lowest 7-day quintiles earn 0.00003 and -0.00005 (t about 0.6), against 0.0029 to 0.0037 (t 3.5 to 4.0) in the top two.
- F6: The book's deepest fall, -35.5%, built up over windows 5 to 10, with drawdowns of -24% to -36%. In those windows the coins' 30-day return averaged 0.021 against 0.056 elsewhere, and their 90-day return 0.087 against 0.196, yet the book was long more often (58% of bars against 49%). The Calmar is 0.42.
