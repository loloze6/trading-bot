---
idea: 002-03_price-cross-above-long-sma
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's close has crossed above its long moving average -> adapted: "after the cross" becomes "while the close is above the long SMA", graded by its percent distance above it.
- Comparison: random bars -> kept: compared with the coin's mean return over all bars of all windows, which is holding the coin.
- Outcome: price keeps rising over the following bars, more often and further -> kept.
- Verdict transfer: yes: the only changes are the two allowed ones ("after" becomes "while", on/off becomes graded), and the outcome and its comparison are measured as stated.
Forecast: The forecast uses one indicator, the percent distance of the close from its 200-day simple moving average. It is standardised against its own past 200 values, so a typical distance gives about 10, capped at 20. It is then clipped at 0, because the idea is only about the cross upward. It is zero while the close is at or below the 200-day SMA. It is positive and grows with how far the close sits above the SMA. It is never negative.
Config: 002-03_price-cross-above-long-sma_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The forecast-weighted excess return, before costs. At each bar, take allocation x (the next 20-bar return minus 20 x the coin's mean daily return pooled over all its windows). Sum this into non-overlapping 20-bar blocks, pool the blocks across coins, and compute the t-statistic of the block mean.
- Supporting check: On bars with forecast > 0, the share whose next 20-bar return beats 20 x the coin's pooled mean daily return, compared with 50 percent.
- Confirm: The block-mean excess return is positive with t >= 2.
- Reject: The block-mean excess return is negative with t <= -2. This means that after the price moves above the average, the move reverses or underperforms holding the coin.
- Inconclusive: Any t between -2 and 2, including results near zero, is inconclusive. So is any run with fewer than 50 non-overlapping 20-bar blocks with a non-zero position, pooled over the coins.
