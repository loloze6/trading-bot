---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close rises above its highest close of the prior 20 days, the coin rises over the next 5 days, and the further the close clears that old high relative to the coin's 20-day daily volatility, the larger the rise.
Consequence: A trader would take a long after daily breakouts above the 20-day closing high, and would refuse to short them as traps.
Why:
- F1: Closes above the prior 20-day closing high are followed by a rise, which is the opposite of the brief: over 799 non-overlapping breakout cases, the 5-day unusual move is +1.34 % (t 3.13) and the total move +1.93 % (t 4.49), about 10 times the 0.19 % cost of a trade. Fresh first-day breakouts alone show the same, mean 0.130 usual moves (t 3.20, 708 cases).
- F2: The rise after a breakout grows with how far the close clears the old high, measured in the coin's daily volatility: 0.048 usual moves (t 0.80) in the smallest third, 0.122 (t 1.76) in the middle and 0.172 (t 2.55) in the largest, 267 cases per third. The rank correlation over all cases is only 0.039, so the grading is coarse.
- F3: Failed breakouts are not followed by a fall: over 619 cases the mean 5-day move is +0.037 usual moves (t 0.98). Thin-volume failures lean the other way, +0.118 (t 1.67, 206 cases), and failure depth shows nothing (deep 0.034, mid 0.054, shallow 0.021).
