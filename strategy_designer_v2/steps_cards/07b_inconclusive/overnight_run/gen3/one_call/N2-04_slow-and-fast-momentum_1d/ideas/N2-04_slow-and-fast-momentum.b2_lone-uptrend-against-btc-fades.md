---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.b inconclusive
backtest: N2-04_slow-and-fast-momentum_1d
instruments: ETH, LTC, XMR, XRP, ZEC, with BTC's daily bars as the market state
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's own 60-day and 20-day returns are both positive but BTC's 60-day return is negative at that close, the coin's next 20 days rise less than its average 20-day return.
Consequence: A trader should treat a coin's lone uptrend against a falling BTC as a trade to refuse, not as momentum.
Why:
- F2: The effect appears when the whole market is trending up too: active blocks where BTC's own 60-bar and 20-bar returns are both positive earn +0.078 mean excess (t 3.09, n 102, trimmed mean +0.052, hit 0.62). Active blocks where BTC is not up on both earn -0.082 (t -2.05, n 37, hit 0.32).
- F3: The split on BTC's 60-bar return alone shows the same pattern: +0.058 (t 2.42, n 118, hit 0.59) with BTC up against -0.094 (t -2.06, n 21, hit 0.24) with BTC down. Inactive blocks are near zero or negative in both states (-0.032, t -1.88, n 153 and -0.003, t -0.11, n 98).
- F5: The edge belongs to the market trend, not to a coin's own strength. With BTC up, alts beat BTC's own forward return by only +0.026 (t 0.85, n 93, median -0.017). Alts whose 60-bar return beats BTC's do no better (+0.066, t 1.06, n 38) than weaker alts (+0.059, t 2.22, n 55).
- F7: The losses come from market-wide down years: 2018 active blocks lost -0.226 (t -3.71, n 12, hit 0.08) and 2022 lost -0.065 (t -1.58, n 14). These are the periods when the coin's own trend fired against a falling BTC.
