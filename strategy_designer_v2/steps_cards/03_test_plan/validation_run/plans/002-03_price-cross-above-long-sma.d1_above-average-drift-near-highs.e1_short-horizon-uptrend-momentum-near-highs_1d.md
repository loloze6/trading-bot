---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin closes above its long moving average -> adapted: a regime rule on the bars spent above the 200-day SMA, with long-only graded sizing inside it.
- Comparison: the nearer the close to the top of its recent range, and the stronger its recent rise, the larger the return -> adapted: both measured continuously (20-bar range position and 20-bar rise) and averaged.
- Outcome: a larger upward return over the following days to two weeks, faded by a month -> adapted: measured at 10 bars; the month-fade holding period is dropped.
- Verdict transfer: yes: the forecast scales the long with the idea's two measures only while the close is above the long average, so its gain at 10 bars is the idea's claim.
Forecast: The forecast is active only while the close is above its 200-day SMA, read as MovingAverageAgeComponent(200) at +1 or more; otherwise it is flat. Inside that regime it averages two parts, each standardised over 60 bars (min 20) and clipped at 0, so the forecast is long only: - where the close sits in its 20-bar closing range (DonchianBreakoutComponent, period 20); - the 20-bar percent rise (PriceEvolutionComponent, period 20). The forecast is 0 when the close is in the lower half of its range and the coin has not risen. It grows smoothly as the close nears the 20-bar high and the rise strengthens, up to about +20.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, on bars in the trending regime. For each case, take the forward 10-bar return minus the coin's mean 10-bar return over all windows. Compare the top half of cases by forecast with the bottom half (Welch t, top minus bottom).
- Supporting check: Cases with forecast above 0 have a mean forward 10-bar excess return (vs the coin's mean) above 0.
- Confirm: The top-minus-bottom difference has Welch t ≥ 2, and the supporting check passes.
- Reject: The top-minus-bottom difference has Welch t ≤ -2: larger forecasts are followed by smaller 10-bar excess returns.
- Inconclusive: Inconclusive if -2 < t < 2, or if t ≥ 2 but the supporting check fails. It is also inconclusive if either half has fewer than 100 grid cases across all coins and windows.
