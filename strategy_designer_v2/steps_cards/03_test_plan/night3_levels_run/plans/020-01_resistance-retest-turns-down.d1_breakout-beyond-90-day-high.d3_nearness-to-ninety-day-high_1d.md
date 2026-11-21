---
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: how close the daily close stands to its highest close of the previous 90 days -> kept: DistanceFromHighComponent, period 90, close, current bar excluded.
- Comparison: closer to the high against farther beneath it -> kept: the distance is centred on its usual size, so nearer than usual is long and farther than usual is short.
- Outcome: the coin rises more over the next 20 days -> kept: each bet is held 20 daily bars.
- Verdict transfer: yes: the forecast grows with nearness to the prior 90-day high and is judged on the 20-day return that follows.
Forecast: The forecast starts from the percent distance of the close from the highest close of the prior 90 bars, with bar t excluded. This distance is negative below the high and positive above it. It is standardised over 90 bars, which gives about -10 at its usual distance, near 0 at the high and above 0 on a new high. It is then averaged at equal weight with the constant +10, so the forecast is (s + 10) / 2. The forecast is 0 when the close sits at its usual distance below the high. It is positive and up to about +5 or more as the close nears or passes the high. It is negative, about -5 at twice the usual distance, as the close falls far beneath the high. It is graded throughout.
Config: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The cases are the bars on a non-overlapping 20-bar grid of each window. For each case, take the coin's 20-bar forward return minus its mean 20-bar return over all windows. Regress that excess return on the forecast at the grid bar, pooled over coins and windows, and take the t of the slope.
- Supporting check: Among the grid cases, the mean excess 20-bar return of the top-quintile forecasts minus that of the bottom quintile is above 0.
- Confirm: The slope t is 2 or more and the supporting check passes (top minus bottom quintile above 0).
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with the quintile difference not above 0, is inconclusive. Fewer than 300 grid cases across all coins and windows is also inconclusive.
