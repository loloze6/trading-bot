---
idea: N2-02_capitulation-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close at an extreme distance below its 200-day average while recent daily volatility is above its usual level -> adapted: the depth below the 200-day SMA is graded with the strongest dead zone, and the volatility condition is kept as a regime (20-day volatility percentile at or above the median of its last 100 days).
- Comparison: rise greater than the coin's normal drift -> kept: forward returns are compared with the coin's mean return over all windows together.
- Outcome: price rises over the next one to two weeks -> kept: the 10-bar forward return after long positions.
- Verdict transfer: yes: the forecast is long only in high-volatility bars, and the position grows sharply only at extreme depth below the 200-day SMA, so the result speaks directly to the idea.
Forecast: The forecast uses two parts. - Volatility gate: the regime is on while the smoothed 20-day volatility percentile, ranked over the last 100 days, is at least 0.5. On all other bars the forecast is flat. - Depth inside the gate: the close's percent distance from its 200-day SMA, standardised over its own past 200 values (min_periods 50) and negated, so a close below the average gives a positive value. It is clipped at 0, so it is long only and zero above the SMA. It then passes through signed_power with exponent 3 and pivot 20. The result is close to zero at moderate depths, about 2.5 at the average depth and up to 20 (200% long) at the deepest plunges, growing smoothly with depth.
Config: N2-02_capitulation-rebound_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The coin's 10-bar forward return after bars with forecast >= 10, minus the coin's mean 10-bar return over all 24 windows together. Results are pooled across coins, and only non-overlapping 10-bar cases are counted.
- Supporting check: The mean 10-bar excess return should rise across forecast buckets (0 to 5, 5 to 10, 10 and above) within the high-volatility regime.
- Confirm: The mean excess return is positive with t >= 2 on at least 30 non-overlapping cases.
- Reject: The mean excess return is negative with t <= -2 on at least 30 non-overlapping cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 non-overlapping cases with forecast >= 10, neither confirms nor rejects the idea.
