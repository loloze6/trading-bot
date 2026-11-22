---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's last 4-hour bar relative to its average 4-hour range over the past 30 days, and the higher that bar's volume relative to its 7-day average, the more the coin rises over the next 3 days.
Consequence: A trader would lean long after unusually wide, heavy-volume bars and avoid longs after narrow, quiet ones.
Why:
- F5: A wide last bar is followed by higher 3-day returns, in a graded way. By quintile of the last 4h bar's range relative to its 180-bar mean, the next-18-bar strength is −0.062, −0.070, +0.006, +0.023 and +0.087 (t −2.24, −2.52, 0.21, 0.73, 2.33; about 1030 cases each). By quintile of last-bar volume relative to its 7-day mean, the top quintile has +0.105 (t 2.99, 1086 cases) and the other four quintiles are all negative.
