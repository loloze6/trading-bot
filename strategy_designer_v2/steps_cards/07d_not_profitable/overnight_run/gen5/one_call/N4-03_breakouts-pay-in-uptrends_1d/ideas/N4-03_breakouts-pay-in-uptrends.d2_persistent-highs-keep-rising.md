---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-03_breakouts-pay-in-uptrends
line: 7.d not profitable
backtest: N4-03_breakouts-pay-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has stayed in the top part of its 20-day close range for several consecutive daily bars, the coin keeps rising over the next 10 days more than it does on average.
Consequence: Enter a breakout only once it has held for a few bars, rather than on the first new-high close that often reverses within two days.
Why:
- F4: Fees are not the cause: the gross sum is 12926 % and the net sum 12560 %, about 0.3 % of commission per trade. The losses come from short holds. The 765 long trades held 2 days or less average −3.18 % before fees (−2430 % summed). Long trades held 10–30 days average +19.0 %, and those held over 30 days +32.0 %.
- F5: Only the largest forecast earns. Long bars with forecast ≥ 10 beat holding by +0.084 over 10 days (t 2.90, 87 cases). The 2–10 bucket earns +0.005 (t 0.39, 225 cases) and the 0–2 bucket −0.013 (t −1.20, 198 cases). Over all trending grid bars, the regime alone earns +0.0023 (t 0.38, 902 cases).
