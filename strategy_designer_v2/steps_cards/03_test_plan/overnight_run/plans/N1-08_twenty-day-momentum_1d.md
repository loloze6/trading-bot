---
idea: N1-08_twenty-day-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: past 20-day return in the top part of its range -> adapted: the 20-day return is used as a graded size instead of a "top part" threshold.
- Comparison: next 20 bars after a high 20-day return vs after a low one -> kept: the signed forecast is long on high returns and short on low ones, so it contrasts the two.
- Outcome: next 20 bars rise further when the 20-day return is high -> kept: measured as the forward 20-bar return against the forecast.
- Verdict transfer: yes: the test measures whether forward 20-bar returns grow with the past 20-day return, which is the idea's claim.
Forecast: The forecast is the coin's 20-bar percent return (PriceEvolutionComponent, period 20). It is standardised against its own previous 60 values, so an average-sized move gives about ±10, capped at ±20. It is positive after a 20-bar rise and negative after a 20-bar fall. It grows in proportion to the size of the move and is zero only when the 20-bar return is zero. It is active on every bar, with no regime gate.
Config: N1-08_twenty-day-momentum_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Regress each bar's forward 20-bar return, minus the coin's mean 20-bar return over all windows together, on that bar's forecast. Pool all coins and windows, and use only every 20th bar so overlapping returns count once. The measure is the t-statistic of the slope.
- Supporting check: The mean forward 20-bar excess return on bars in the top fifth of forecasts, minus the same mean on bars in the bottom fifth, pooled over all coins and windows.
- Confirm: The slope t-statistic is 2 or more, and the top-minus-bottom difference is positive.
- Reject: The slope t-statistic is -2 or less, meaning high past returns are followed by smaller forward 20-bar returns than low ones.
- Inconclusive: Any slope t-statistic between -2 and 2 is inconclusive. Fewer than 300 non-overlapping 20-bar cases in total is also inconclusive.
