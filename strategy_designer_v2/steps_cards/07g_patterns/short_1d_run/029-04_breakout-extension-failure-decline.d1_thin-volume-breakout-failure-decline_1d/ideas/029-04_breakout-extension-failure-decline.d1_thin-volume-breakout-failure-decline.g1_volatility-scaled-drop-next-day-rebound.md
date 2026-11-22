---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
line: 7.g patterns
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close falls sharply against its own volatility of the previous 20 days, the coin rises over the next day. The larger the fall in units of that volatility, the larger the rise.
Consequence: Refuse to short a coin the day after an outsized volatility-adjusted drop, and treat such drops as a reason to lean long over the following day.
Why:
- F1: The day after a coin's sharpest falls, measured against its own prior 20-day volatility (the lowest decile of the day's return divided by that volatility), the coin's next-day return beats its normal daily drift by +0.52 % (median +0.60 %, t 3.51, 1440 days). The effect survives trimming the 5 % tails on each side (t 4.03), is positive in all six coins (+0.23 % BTC to +0.90 % XMR, t 2.90) and in 7 of 8 years.
- F2: The effect is graded. The next decile up gives +0.26 % (t 2.12), the third +0.08 % (t 0.59), and the middle deciles about zero to negative. Across the 7056 down days, the Spearman correlation between the fall's size in volatility units and the next day's unusual return is +0.064.
- F4: Sorting failures by breakout-day volume runs against the tested idea's grading. The thin tercile falls only 0.65 % (t -0.47, 57 cases) and the heavy tercile rises 0.87 % (t 0.72). Deep failures, closing furthest below the old high, rebound by +2.35 % (t 1.61, 57 cases).
