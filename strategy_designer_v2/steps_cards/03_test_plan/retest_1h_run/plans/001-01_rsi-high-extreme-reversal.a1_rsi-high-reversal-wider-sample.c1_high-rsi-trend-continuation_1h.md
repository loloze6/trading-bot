---
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: 14-day RSI standing above 50, the higher the stronger -> adapted: graded RSI minus 50 (RSI over 336 hourly bars), zero at or below 50
- Comparison: a rise above the coin's usual move, strongest while the 60-day return is positive -> kept: forward return minus the coin's mean return, split by the sign of the 1440-bar return
- Outcome: price rises more than usual over the next 10 days -> kept: the 240-bar forward return of the coin, upward
- Verdict transfer: yes: the forecast grows with RSI above 50 exactly as stated, and the 60-day trend split is recorded as the regime.
Forecast: The forecast is 50 minus the 336-bar Wilder RSI, with its sign flipped, so it is RSI minus 50. It is standardised against its own past 337 values and clipped at 0. It is therefore zero when RSI is at or below 50. It is positive and grows linearly as RSI rises above 50, up to the cap of 20. The detector labels a bar `trending` when the 1440-bar (60-day) return is above 0, and `unknown` otherwise. Both regimes hold the identical component, so the position never jumps at the regime change; the regime only records the 60-day trend for the split.
Config: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h_config.json
Criterion:
- Horizon: 240 bars
- Main measure: The slope, with its t, of the coin's 240-bar forward return minus that coin's mean 240-bar return over all windows, regressed on the forecast. It is measured on non-overlapping 240-bar grid bars, pooled over coins and windows, before costs.
- Supporting check: The same slope on `trending` bars minus the slope on `unknown` bars, as a Welch t.
- Confirm: The main slope has t ≥ 2, and the supporting difference has t ≥ 2.
- Reject: The main slope has t ≤ -2.
- Inconclusive: Any main slope with t between -2 and 2 is inconclusive. A main slope with t ≥ 2 whose supporting difference has t below 2 is also inconclusive. At least 300 grid cases with a forecast above 0 are needed, and at least 100 of them in each regime; with fewer, the result is inconclusive.
