---
idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: close's distance from the middle of its 30-day closing range -> kept
- Comparison: flatness of the 30 days (net move small against the range) scales the move -> kept
- Outcome: move away from the middle, same direction, over the next 5 days -> kept
- Verdict transfer: yes: the forecast is exactly position-in-range times flatness, held 5 days in the continuation direction, so its forward returns confirm or reject the idea as stated.
Forecast: The forecast uses one component, FlatnessWeightedRangePositionComponent with period 30, which reads the last 31 daily closes. Its raw value is (2 x pos − 1) x (1 − |close[t] − close[t−30]| / (H − L)): - the first factor is where the close sits in its 30-day closing range, from −1 at the low to +1 at the high; - the second factor is how flat the month was, near 1 when the net move is small against the range. The raw value is then standardised over its past 60 values (target 10, cap 20) and is not negated, so it follows the move (continuation): - it is positive, long, when the close sits above the middle of a flat month; - it is negative, short, when the close sits below the middle; - it is near zero at the middle of the range or after a one-way month; - its size grows continuously with the distance from the middle and with the flatness. It is active on every bar, with no regime.
Config: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope, and its t, from a least-squares fit of the coin's 5-bar return minus its normal 5-bar drift on the bar's forecast. The cases are bars on the non-overlapping 5-bar grid of each window, all coins pooled.
- Supporting check: The book's timing gain must be above zero: its mean daily return before costs minus the gain from the market's own rise.
- Confirm: The idea is confirmed when both hold: - the slope is positive with t ≥ 2; - the timing gain is above zero.
- Reject: The slope is negative with t ≤ −2: price reverts toward the middle in proportion to the forecast.
- Inconclusive: Any slope with |t| < 2 is inconclusive, and so is a positive slope with t ≥ 2 whose timing gain is not above zero. At least 300 grid cases are required across coins and windows; with fewer, the result is inconclusive.
