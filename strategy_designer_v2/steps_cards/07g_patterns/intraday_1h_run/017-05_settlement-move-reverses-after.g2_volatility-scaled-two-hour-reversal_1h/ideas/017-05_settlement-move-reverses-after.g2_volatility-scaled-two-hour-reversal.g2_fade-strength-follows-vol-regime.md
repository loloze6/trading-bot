---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 2-hour move reverses over the next 2 hours by an amount that grows with its 7-day hourly volatility relative to its own ~3-week level, and the reversal is largest when volatility is far above its norm.
Consequence: Short-term fading is only worth paying fees for when a coin's volatility is well above its recent norm.
Why:
- F3: Among the 20% largest 2-hour moves, the 2-hour fade rises steadily with 7-day volatility relative to its ~3-week median, by quintile: 1.0 bp (t 0.6), 4.2 bp (t 2.4), 7.7 bp (t 3.9), 8.7 bp (t 3.6), 17.4 bp (t 5.5), with about 7640 cases each.
- F1: The book's gross gain before costs is 0.97 bp per bar, while fees cost 4.34 bp per bar on a turnover of 0.40 of the book per bar, so the mean daily book return is -80.4 bp against the coins' +11.9 bp over 17381 coin-days; the edge that was confirmed is real but far too thin for hourly rebalancing.
- F4: Among large moves, the fade is small and not distinct from zero in BTC (1.5 bp, t 0.9) and ETH (2.5 bp, t 1.2). It is 8 to 14 bp in LTC, XMR, XRP and ZEC (t 3.6 to 4.6).
