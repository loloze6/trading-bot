---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes back below its old 20-day high within 3 days of closing above it, the coin rises over the next 10 days, the more so the larger that day's fall in units of the coin's 20-day daily volatility.
Consequence: A trader would treat a failed daily breakout as a reason to refuse a short, since it has been followed by a rebound rather than further decline.
Why:
- F4: My own reconstruction of the tested situation does not reproduce the step-5 result. Read on the bar of the close back below the old 20-day high, the coin rises +2.59 % from day 2 to day 10 (t 3.08, 386 events) and +3.22 % from day 0 to day 10 (t 3.39). On the 8-day grid, failure cells show an excess rise of +4.56 % (t 2.71, 131 cases).
- F5: The book's short trades lose on every coin. Mean net trade results run from -0.56 % (XMR) to -3.57 % (ZEC), and only 34.9 % of 878 trades win. This fits F4 better than the confirmed excess fall of the verdict, so the two case definitions should be compared before the verdict is trusted.
- F1: The day after a coin's daily return falls in the lowest tenth when measured in units of its 20-day daily volatility, the coin beats its normal daily drift by +0.53 % (t 3.61, 1450 days). The effect shrinks steadily across the deciles: the second tenth gives +0.27 % (t 2.18), the middle tenths are near 0, and the seventh to ninth tenths are negative (-0.25 %, t -2.26 in the eighth).
