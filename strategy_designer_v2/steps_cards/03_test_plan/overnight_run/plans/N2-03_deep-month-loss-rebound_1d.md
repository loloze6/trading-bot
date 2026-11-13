---
idea: N2-03_deep-month-loss-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin has fallen sharply over 20 days -> adapted: "sharply" becomes graded, so the size of the 20-day fall sets the position, and "after" becomes "while".
- Comparison: the next 20-day rise exceeds the coin's usual 20-day move -> kept: forward returns are judged against the coin's mean 20-day return over all windows.
- Outcome: price rises over the next 20 days -> kept: the forward 20-bar return of a long position.
- Verdict transfer: yes: the forecast is long only in proportion to the depth of the 20-day fall, so its forward returns answer the idea directly.
Forecast: The forecast starts from the 20-bar percent price change (PriceEvolutionComponent, period 20), standardised against its own past 60 values and negated. A 20-day fall therefore gives a positive value and a rise gives a negative one. Clipping at a minimum of 0 keeps only the decline side, so the forecast is long or flat, zero when the coin has risen. signed_power with exponent 3 (pivot 10) damps small and ordinary declines to near zero and amplifies deep ones. The long position grows steeply with the depth of the fall relative to the coin's recent 20-day moves. No regime is used.
Config: N2-03_deep-month-loss-rebound_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The coin's forward 20-bar return after bars in the top decile of positive forecast, pooled over coins and windows, minus that coin's mean 20-bar return over all test windows together. The t-statistic counts overlapping 20-bar returns once, so it uses non-overlapping episodes.
- Supporting check: Across all bars with a nonzero forecast, the slope of forward 20-bar excess return on forecast size is positive.
- Confirm: The mean excess forward return after top-decile forecasts is positive with t ≥ 2.
- Reject: The mean excess forward return after top-decile forecasts is negative with t ≤ -2, meaning deep falls keep falling more than usual.
- Inconclusive: Any t between -2 and 2, including estimates near zero. The test also needs at least 30 non-overlapping 20-bar top-decile episodes across all coins; with fewer, the result is inconclusive whatever its t.
