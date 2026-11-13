---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.d not profitable
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, when a second large daily drop follows a first one on the next day, the following close rebounds more strongly and more often than after a single large drop.
Consequence: Put the largest rebound positions after consecutive capitulation days, not on every capped single drop.
Why:
- F4: A larger forecast earns more only up to the cap. Mean next-day return rises from +0.40% (forecast 2–8, n=1515) to +0.83% (8–16, n=594) and +1.49% (16–20, n=181). The capped bars at 20 earn only +0.62% (n=1099), yet they carry the largest position (about 2.0x), so the biggest bets earn less per unit of risk.
- F7: A second consecutive large drop is followed by a much stronger next-day rebound, +2.68% (t 4.96, n=148, hit 70%), than a first large drop, +0.49% (t 2.87, n=1132).
