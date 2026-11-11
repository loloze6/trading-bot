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
- Situation: the close has crossed above its long moving average -> adapted: "after the cross" becomes "while the close is above its 200-day SMA", sized by the percent distance above it.
- Comparison: compared with random bars -> kept: forward returns on positioned bars are judged against all bars (holding the coin).
- Outcome: price keeps rising more often and further over the following bars -> kept: the sign and size of forward returns after positioned bars.
- Verdict transfer: yes: the up-cross has only been turned into the graded "above the long average" state the guide allows, and both the frequency and the size of rises are measured.
Forecast: The forecast is the percent distance of the close above its 200-day SMA. It is standardised against its own previous 200 values, then clipped at 0 so it is long only. It is 0 whenever the close is at or below the SMA. It is positive above the SMA, starting near 0 at the cross and growing smoothly as the price moves further above the average, capped at 20. It is never negative.
Config: 002-03_price-cross-above-long-sma_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The forward 10-bar return of the coin after bars with forecast > 0, minus the coin's mean forward 10-bar return over all bars in the same window. Results are pooled over coins and windows, using non-overlapping 10-bar blocks, and the t-statistic is taken on that excess. This is measured before costs.
- Supporting check: On positioned blocks, the share of forward 10-bar returns above 0 minus the share across all blocks. Separately, the slope of forward return on forecast size should be positive.
- Confirm: The mean excess forward return is above 0 with t ≥ 2. The supporting hit-rate difference must also be above 0.
- Reject: The mean excess forward return is below 0 with t ≤ -2. This would mean moves above the average reverse more than they persist.
- Inconclusive: Any t between -2 and 2 is inconclusive, including results near zero. So is any result from fewer than 100 non-overlapping positioned 10-bar blocks pooled, or fewer than 10 per coin.
