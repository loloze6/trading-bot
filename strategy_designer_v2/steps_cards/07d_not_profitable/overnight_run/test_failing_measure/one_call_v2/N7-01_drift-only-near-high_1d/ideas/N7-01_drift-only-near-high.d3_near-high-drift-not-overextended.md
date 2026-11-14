---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, except when the coin has already risen by a very large amount over the prior 30 days.
Consequence: Refuse the near-high long after an outsized 30-day run, where the excess return vanishes and the volatility, and with it the risk of a fall, is greatest.
Why:
- F6: The edge fades when the trend is already stretched; these figures are mean per-coin book returns on active days, not the book's daily return.
