---
idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: the close sits far above the middle of its 30-day closing range -> kept
- Comparison: the 30 days were flat, a small net move against the range -> kept
- Outcome: a larger rise over the next 5 days, upward only (no short near the bottom) -> kept
- Verdict transfer: yes: the forecast is exactly range position times flatness over 30 closes, held long-only for 5 days, so its 5-day gains confirm or reject the idea.
Forecast: The forecast uses `FlatnessWeightedRangePositionComponent` with period 30 on daily closes. Its value is (2 x position in the 30-day closing range − 1) x (1 − |net 30-day move| / closing range). It is standardised over its past 60 values (min_periods 20), then clipped at 0 so it stays long only. It is positive when the close is above the middle of a flat 30-day range. It grows as the close nears the top and as the month gets flatter. It is zero at or below the middle, and when a strong one-way move cancels the flatness factor. There is no regime and no dead zone, because the idea is a steady relation.
Config: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, all coins and windows pooled. On it, regress the coin's 5-day forward return, minus that coin's mean 5-day return over all windows, on the recorded forecast. The measure is the slope's t, before costs.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2: larger forecasts are followed by larger rises above the coin's normal drift.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is any result with fewer than 200 grid cases with forecast > 0.
