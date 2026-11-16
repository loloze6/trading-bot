---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: close above its 200-day average, with a 10-day return large against 20-day daily volatility -> kept: the 200-day condition is a regime; the vol-scaled 10-day return is graded.
- Comparison: larger vol-scaled return against smaller -> kept: position size grows with the vol-scaled return.
- Outcome: larger rise over the next 10 days -> kept: 10-bar forward return, judged against the coin's average.
- Verdict transfer: yes: the test measures the same quantities, the same condition and the same horizon the idea states.
Forecast: The regime is trending while the close is above its 200-day simple average, and flat otherwise. In the trending regime the forecast is the 10-day return divided by (20-day standard deviation of daily returns × √10). This is VolatilityScaledReturnComponent with period 10 and vol_period 20. It is standardised over its own past 60 values (target 10, cap 20) and clipped at 0, so the forecast is long-only as the consequence states. It is zero when the 10-day move is down or the close is below the average, and it grows linearly with the size of the volatility-adjusted gain.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use a non-overlapping 10-bar grid in each window and keep the bars where the regime is trending. Regress each bar's forward 10-bar return minus the coin's mean 10-bar return (all windows) on the forecast at that bar, pooled over coins, and read the slope's t.
- Supporting check: The book's timing gain (its mean daily return minus the part from the market's own rise) is above 0 before costs.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a timing gain of 0 or less, is inconclusive. Any result from fewer than 100 trending grid cases pooled across coins is also inconclusive.
