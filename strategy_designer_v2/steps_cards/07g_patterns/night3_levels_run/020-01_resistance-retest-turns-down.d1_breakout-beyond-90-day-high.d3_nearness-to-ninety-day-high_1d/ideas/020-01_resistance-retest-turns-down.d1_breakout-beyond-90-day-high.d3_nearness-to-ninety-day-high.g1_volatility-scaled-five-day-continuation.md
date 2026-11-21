---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 5-day return measured against its own daily volatility over the past month, the more the coin rises over the next 10 days.
Consequence: A trader should lean long after a coin's unusually strong 5-day rise and lean away from it after an unusually weak one, holding about ten days, since the following move is many times a trade's cost.
Why:
- F1: Measured on non-overlapping 10-day grids, a coin's 5-day return scaled by its own volatility over the prior 30 days predicts its excess 10-day return: the slope is +0.10 of the coin's usual 10-day move per unit of scaled return, t 3.50 on 1115 independent cases. This stands out among the roughly 20 angles tried. The same measure gives t 2.23 over 5 days (2411 cases) and t 0.67 over 20 days (539 cases), so the continuation fades by the third week.
- F2: The size of the scaled move also carries information without its sign: the absolute 5-day scaled return predicts the excess 10-day return with t 2.92 (1115 cases). Together with F1, this means large 5-day rises are followed by the largest gains, and large falls by somewhat above-normal returns. The overlapping 5-day table agrees: after daily moves beyond 2 of their usual size, the mean 5-day return is +2.26 % after rises and +0.64 % after falls, against about +0.3 % after small moves.
- F6: Scaled 1-day moves do not predict 20-day returns (slope t -1.08, 539 cases; per coin from -1.27 to +0.72). Volatility quintiles and position in the 60-day range show no ordered pattern (pooled slope t 0.61 and 0.15).
