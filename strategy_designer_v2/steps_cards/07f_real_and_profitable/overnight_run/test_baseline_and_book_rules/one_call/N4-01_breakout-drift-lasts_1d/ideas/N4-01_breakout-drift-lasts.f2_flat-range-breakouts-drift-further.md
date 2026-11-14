---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, a new 20-day closing high reached after only a small rise over the prior 20 days, so a break out of a flat range, is followed by a larger ten-day rise than a new high reached after a steep prior run.
Consequence: A trader would favour breakouts from flat ranges and size down on highs that come at the end of an already steep climb.
Why:
- F8: New highs reached after the weakest prior 20-day rise drift more: the lowest per-coin momentum tercile gives a mean excess of 0.0277 (t 2.09, n 149), against 0.0116 (t 0.73, n 151) in the highest tercile.
- F2: The confirmed drift rests on a few events: on 445 non-overlapping new-20-day-high events the mean excess 10-bar return is 0.0214 (t 2.49), but without the 10 largest it is 0.0035 (t 0.56, n 435), and the median event is -0.0128.
