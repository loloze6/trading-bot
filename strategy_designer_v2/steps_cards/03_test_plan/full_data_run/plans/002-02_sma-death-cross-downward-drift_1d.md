---
idea: 002-02_sma-death-cross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short moving average has crossed below the long one -> adapted: "after the cross" becomes "while the 50-day SMA is below the 200-day SMA", graded by how far below.
- Comparison: price after random bars -> kept: compared with the coin's mean return over all bars of all windows (holding).
- Outcome: price keeps falling, more often and further -> kept: the short position's forward return against holding.
- Verdict transfer: yes: a short sized by the spread below the long average gains beyond holding only if price keeps falling while the cross holds; it loses if moves reverse.
Forecast: The forecast uses one indicator, the spread between the 50-bar SMA and the 200-bar SMA of the close, in percent of the 200-bar SMA. These are the conventional daily cross settings. The spread is standardised against its own past 200 values and then clipped at a maximum of 0. The forecast is therefore 0 while the short average is at or above the long average. It is negative (short) while the short average is below the long one, and the short grows smoothly as the short average falls further under the long one, capped at -20. It is never positive.
Config: 002-02_sma-death-cross-downward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On bars where the forecast is below 0, take the coin's forward 10-bar return minus holding. Holding is the coin's mean 10-bar return over all windows of that coin together. Weight each case by |forecast| and pool across coins. Use non-overlapping cases only (one bar in 10), and report the t-statistic of the short side's excess gain.
- Supporting check: Split the short cases into terciles of |forecast|. The excess gain of the short in the top tercile should be larger than in the bottom tercile.
- Confirm: The short side's weighted mean excess gain is above 0 with t ≥ 2. Price falls further than holding while the short average is below the long one.
- Reject: The short side's weighted mean excess gain is below 0 with t ≤ -2. Price rises relative to holding after downward crosses, meaning moves reverse.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive, including results near zero. Fewer than 30 non-overlapping short cases in total is also inconclusive.
