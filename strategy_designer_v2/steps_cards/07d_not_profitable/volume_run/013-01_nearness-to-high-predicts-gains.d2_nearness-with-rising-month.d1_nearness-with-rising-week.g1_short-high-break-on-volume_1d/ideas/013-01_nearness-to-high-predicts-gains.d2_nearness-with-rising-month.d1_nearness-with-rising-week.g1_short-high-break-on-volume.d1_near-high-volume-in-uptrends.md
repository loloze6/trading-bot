---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the higher the coin's return over the next 7 days, only while the coin's own 60-day return is positive, the gain growing with both closeness and volume inside that rising state.
Consequence: Hold larger longs in coins pressing their 20-day high on heavy volume during a rising 60-day trend, and do not read a close far below the high as a reason to short.
Why:
- F1: The book's whole gain comes from its long side. Long bars summed +6.32 in gain before fees against 1.13 in fees. Short bars summed −0.36 before fees and paid another 0.79 in fees, so after fees the shorts are a net loss of about 1.14 over 8,517 bars.
- F2: Removing the shorts repairs the failing Calmar but not the mean. A long-only version of the same book has mean daily return 0.000296 against 0.000229, Sharpe 1.02 against 0.61, deepest fall −13.3% against −19.8%, and Calmar 0.81 against 0.39 (the rule needs 0.75).
- F4: Only the top forecast quintile carries real gains: +1.84% in 7-day excess return (+2.75% raw), with 0.155% daily gain per bar. The next quintile earns 0.026% a day and the lower three about 0 or negative.
- F6: The graded relation is stronger when the coin is rising over 60 days, and so are the long gains:
