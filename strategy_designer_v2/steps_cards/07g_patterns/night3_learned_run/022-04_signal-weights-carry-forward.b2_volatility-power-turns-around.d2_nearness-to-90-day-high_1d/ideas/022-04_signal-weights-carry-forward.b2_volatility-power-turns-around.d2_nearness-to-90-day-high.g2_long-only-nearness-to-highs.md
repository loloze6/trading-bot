---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days, with the rise growing as nearness grows on the long side only.
Consequence: Nearness to the 90-day high is a reason to be long in proportion to nearness, and a close far below the high is a reason to stay out rather than to short.
Why:
- F4: The tested nearness forecast's edge sits on its long side. On grid cases with a positive forecast the slope is 0.046 (t 1.85, 1727 cases), with a negative forecast 0.027 (t 1.13, 1692 cases); the pooled slope is 0.036 (t 2.10). The top forecast fifth carries the gain (+1.05 % over 5 days, t 2.13), while the bottom fifth is only -0.14 % (t -0.34).
- F5: The book is short 47 % of its bars, and that side costs it. Long bars earn +0.038 % per bar, of which 0.018 % is market rise. Short bars lose -0.012 % per bar, mostly the -0.016 % of drift given up by shorting a rising coin. The book's mean daily return is 0.011 % against holding's 0.118 %, and it beats holding in 42 % of windows.
