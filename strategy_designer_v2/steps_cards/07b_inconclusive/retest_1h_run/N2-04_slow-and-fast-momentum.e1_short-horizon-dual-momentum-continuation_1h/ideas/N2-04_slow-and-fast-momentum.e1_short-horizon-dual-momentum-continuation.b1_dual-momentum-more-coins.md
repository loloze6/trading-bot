---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
line: 7.b inconclusive
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 60-day and 20-day returns are both positive, its next few days' returns are higher than its average daily return, so the continuation shows up at a short horizon rather than over the following 20 days.
Consequence: A trader can hold a coin long over the next days while both its slow and fast returns are up, and stay flat otherwise, to collect short-horizon continuation and avoid its falling stretches.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: the mean excess 72-hour return at forecast > 0 is +0.00371 with t 1.66 over 1858 independent cases, while off-situation bars average −0.00180 (t −1.42, 3825 cases), and the on-minus-off difference has a Welch t of 2.15.
- F2: The effect has the same sign at every horizon tried, with similar strength, so the 3-day horizon is not mislocated: the in-situation excess return is +0.00159 at 24 hours (t 2.22, 5648 cases), +0.0101 at 168 hours (t 1.81, 792 cases) and +0.0224 at 480 hours (t 1.15, 261 cases).
- F3: The effect is positive in all six coins but small in each one: per-coin means run from +0.0003 (LTC, t 0.06, 301 cases) to +0.0082 (ZEC, t 1.11, 281 cases), and no coin reaches t 1.2, so too few cases per coin is what limits the test, not one coin.
- F4: Market swings between periods drown the effect: the in-situation excess is −0.032 in 2018 (t −2.06, 71 cases) and −0.017 in 2022 (t −2.40, 117 cases) against +0.0127 in 2020 (t 2.62, 337 cases), and window means range from −0.062 (w7) to +0.041 (w24).
