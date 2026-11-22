---
idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the close's position in its 30-day closing range, in a coin whose 90-day return is positive -> kept: a 30-bar closing-range position, active only while the 90-bar return is above 0 (a regime).
- Comparison: a higher position in the range against a lower one -> kept: the forecast is graded by the range position.
- Outcome: the coin rises more over the next 5 days -> kept: 5-bar forward return, horizon 5 bars.
- Verdict transfer: yes: the test measures the stated range position, under the stated 90-day condition, against the stated 5-day move.
Forecast: A regime rule sends a bar to `trending` when the coin's 90-bar percent return is above 0. Every other bar goes to `unknown`, which is flat. In `trending`, the forecast is where the close sits in its last 30 closes, bar t included (`DonchianBreakoutComponent`, period 30). It is standardised over its past 60 values, so its average size is about 10, capped at ±20. The forecast is positive above the range's middle and grows to its largest at the top of the range. It is negative below the middle and grows to its most negative at the bottom. It is near 0 at the middle.
Config: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the bars where the regime is `trending`, on a non-overlapping 5-bar grid in each window. Take the slope t of a regression of the coin's 5-bar forward return, minus its mean 5-bar return over all windows, on the forecast at bar t. Pool all coins.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, on at least 200 independent grid cases.
- Reject: The slope is negative with t ≤ -2, on at least 200 independent grid cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is any result on fewer than 200 independent trending-regime grid cases.
