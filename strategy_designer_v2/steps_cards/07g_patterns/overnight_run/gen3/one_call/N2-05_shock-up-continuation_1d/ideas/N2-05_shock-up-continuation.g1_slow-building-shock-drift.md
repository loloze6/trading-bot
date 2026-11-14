---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes up by more than about twice its trailing 20-day mean absolute daily return, its price keeps drifting up over the following two weeks, more than over the first five days.
Consequence: A trader buying big up days should hold for about ten days and not exit after one to five, because most of the drift comes later.
Why:
- F1: After big up days the drift builds beyond the plan's 5-bar horizon. For days of 2 to 3 times the trailing 20-day mean absolute return, the 10-bar excess return is +3.61% (t 3.52, 445 de-duplicated events) against +1.36% at 5 bars (t 2.31). For days above 3 times, it is +3.12% at 10 bars (t 2.64, 334 events) against +0.83% at 5 bars (t 1.24). Events are merged within 5 bars, so the 10-bar windows can overlap partly.
- F8: The book's losses come from one-day trades. Trades lasting up to 1.5 days number 1730 and average -1.11% net. Trades lasting 1.5 to 3.5 days (328) average +7.74%, and trades lasting 3.5 to 10 days (292) average +8.77%. The book still has a Sharpe of -0.24 overall.
