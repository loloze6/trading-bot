---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above the highest high of its prior 20 days, the larger its own 10-day return, the further its price rises over the next 10 days.
Consequence: A trader would size upside breakouts by the strength of the run that carried price through the prior high, not by how far the close clears that high.
Why:
- F4: Breakouts as a group do rise more than usual, but without grading by distance. The mean excess 10-day return after any close above the prior 20-day high is +0.064 (t 2.78, 108 cases, 59 % positive, median +0.040), against −0.004 on the 1,583 cases without a breakout.
- F5: The forecast terciles show no grading. Mean excess returns are +0.079, +0.014 and +0.101 from lowest to highest, and the top 8 forecasts have a mean of +0.244 but a median of −0.012 with half positive, so the largest forecasts are a lottery.
- F7: Among breakouts, the coin's own prior 10-day return grades the next 10-day excess return better than the distance does: slope t +3.14, rank correlation +0.15, 98 cases. Over all grid cases the same slope is t +3.39 (1,547 cases), but with a rank correlation of only +0.06.
