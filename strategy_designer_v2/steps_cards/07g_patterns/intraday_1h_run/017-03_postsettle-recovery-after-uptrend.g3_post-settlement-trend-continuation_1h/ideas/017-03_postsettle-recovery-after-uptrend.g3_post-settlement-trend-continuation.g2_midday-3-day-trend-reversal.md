---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 2 hours from 13:00 UTC, a coin moves against its own 3-day return, and the larger that 3-day return, the larger the move against it.
Consequence: Lean against the 3-day trend in the early UTC afternoon rather than with it.
Why:
- F4: Around midday UTC the 3-day trend reverses rather than continues: for the bar stamped 12:00 the slope of the 2-hour excess return on the 3-day standardised return is -5.89 bp (t -5.3, 16,829 cases); it is negative in all six coins (t from -0.68 to -4.46) and in seven of eight years, with five years at t ≤ -2.4; the neighbouring hours 11:00 (t -4.3) and 13:00 (t -3.4) agree.
