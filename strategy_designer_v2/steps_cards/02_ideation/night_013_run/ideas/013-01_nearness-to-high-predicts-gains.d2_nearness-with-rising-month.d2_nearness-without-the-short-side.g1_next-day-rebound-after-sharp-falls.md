---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day.
Consequence: A trader can buy a coin's sharpest volatility-scaled down days for a one-day rebound, and should avoid selling into them, in any regime.
Why:
- F1: The larger a coin's one-day fall measured against its own 20-day volatility, the larger the next day's return, and the effect is graded across the deciles: the lowest decile is followed by a mean next-day return of 0.0064 (t 4.35, n 1400), the second by 0.0038 (t 3.10), the third by 0.0016 (t 1.20), and the middle deciles by about 0.0003 to 0.0009 (t below 1.2).
- F2: This rebound after a large fall shows in every coin and every year, so it is not carried by one coin or one period: next-day means after the lowest decile run from 0.0037 (BTC) to 0.0100 (XMR, t 3.33), all positive, and from 0.0005 (2024) to 0.0163 (2020, t 3.04), all eight years positive.
- F3: The rebound holds in both regimes the strategy uses. It is 0.0050 (t 3.58, n 1186) in the trending state and 0.0052 (t 3.96, n 1610) in the flat state, so it is independent of the 30-day-return filter the idea relies on.
- F4: The rebound is short-lived. On a non-overlapping 3-day grid, the lowest quintile of scaled daily moves gains only 0.0039 excess over 3 days (t 1.29, n 920), against the one-day effect in F1, so most of the bounce lands on the first day.
