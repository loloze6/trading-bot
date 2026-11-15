---
idea: 002-03_price-cross-above-long-sma.b2_above-average-with-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day SMA, the further the stronger, while the 20-day return is positive, the larger the stronger -> adapted: "while 20d return > 0 and close above SMA200" is a regime; inside it, distance and 20d return are graded and averaged.
- Comparison: the coin's usual drift -> kept
- Outcome: price rises more than usual over the next 20 days -> kept
- Verdict transfer: yes: the forecast grows with both stated quantities only while both conditions hold, and is judged on the excess 20-day return.
Forecast: A regime rule sets the bar to "trending" only when the close is at or above its 200-day SMA and the 20-day return is above 0. On all other bars the forecast is 0 (flat). In the trending regime the forecast is the equal-weight mean of two parts, each clipped at 0. The first is the percent distance of the close above its SMA200, standardised over 200 bars. The second is the 20-day percent return, standardised over 60 bars. Both parts are near 0 at the regime's edges, so the position starts near zero and is long only. It grows as the close moves further above the average and as the 20-day return grows.
Config: 002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Use the non-overlapping 20-bar grid of each window and keep the cases with forecast > 0. For each case, take the coin's 20-bar forward return minus that coin's mean 20-bar return over all windows. Regress this excess return on the forecast and read the slope's t.
- Supporting check: The mean excess 20-bar return of the active cases, weighted by forecast, is above 0.
- Confirm: Slope t >= 2 and the supporting check passes.
- Reject: Slope t <= -2, or the forecast-weighted mean excess return has t <= -2.
- Inconclusive: Any other result, or fewer than 30 active non-overlapping cases.
