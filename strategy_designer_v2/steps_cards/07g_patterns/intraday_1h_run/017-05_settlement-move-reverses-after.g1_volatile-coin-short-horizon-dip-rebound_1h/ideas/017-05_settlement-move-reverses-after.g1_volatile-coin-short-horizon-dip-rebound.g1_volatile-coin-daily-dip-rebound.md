---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 7-day mean absolute hourly move is high, the larger its 1-day fall measured in its usual 1-day moves, the larger its rise over the next 1 to 3 days.
Consequence: A deep one-day drop in a volatile coin is a reason to buy for a multi-day rebound, held long enough that fees no longer swamp the gain.
Why:
- F3: The reversal also holds over a day: in the high-volatility regime, the 24-hour fall's slope on the next 24-hour excess return is positive in all six coins (t from 2.72 for LTC to 4.95 for ZEC, about 1,000–1,100 cases each), but not in the low regime (t from -0.71 to 0.77); the bottom decile of the 24-hour move gains 167.75 bp (t 5.62, n 635).
- F4: On a non-overlapping 72-hour grid within each coin's top volatility tercile, a 24-hour fall predicts gains over the next 24, 48 and 72 hours (t 5.74, 4.07, 4.93); the slope is positive in 6 of 8 years, though 2022 is negative (t -2.02). Only the largest-fall quintile carries it (146.78 bp, t 3.62); the other quintiles sit between -28 and -2 bp.
- F1: The book's loss comes from trading costs, not from a missing edge: the hourly position times the next bar's return sums to between 2.49 (ETH) and 4.78 (XRP) per coin before fees, but fees sum to between 5.96 and 7.98 per coin, and the 68,468 trades (median 2 hours) average -0.163% gross and -0.263% net.
