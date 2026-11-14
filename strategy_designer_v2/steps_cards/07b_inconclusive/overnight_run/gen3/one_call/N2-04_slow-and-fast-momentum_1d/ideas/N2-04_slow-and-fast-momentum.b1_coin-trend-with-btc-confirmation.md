---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.b inconclusive
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, with BTC's daily bars as the market state for each coin
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's own 60-day and 20-day returns are both positive and BTC's 60-day and 20-day returns are also both positive at the same close, the coin's next 20 days rise more than its average 20-day return.
Consequence: A trader should take a coin's trend-following long only when BTC is trending up as well, and refuse it when BTC is not.
Why:
- F2: The effect appears when the whole market is trending up too: active blocks where BTC's own 60-bar and 20-bar returns are both positive earn +0.078 mean excess (t 3.09, n 102, trimmed mean +0.052, hit 0.62). Active blocks where BTC is not up on both earn -0.082 (t -2.05, n 37, hit 0.32).
- F3: The split on BTC's 60-bar return alone shows the same pattern: +0.058 (t 2.42, n 118, hit 0.59) with BTC up against -0.094 (t -2.06, n 21, hit 0.24) with BTC down. Inactive blocks are near zero or negative in both states (-0.032, t -1.88, n 153 and -0.003, t -0.11, n 98).
- F4: Within the BTC-up active blocks the sign is positive in every coin, from LTC +0.025 to XRP +0.142, with ETH strongest (+0.073, t 2.06, n 24, hit 0.79). It is positive in 5 of 7 years, with 2022 (-0.119, n 6) and 2023 (-0.011, n 29) the exceptions. The per-window means are positive in 10 of 16 windows (t 1.02).
- F7: The losses come from market-wide down years: 2018 active blocks lost -0.226 (t -3.71, n 12, hit 0.08) and 2022 lost -0.065 (t -1.58, n 14). These are the periods when the coin's own trend fired against a falling BTC.
