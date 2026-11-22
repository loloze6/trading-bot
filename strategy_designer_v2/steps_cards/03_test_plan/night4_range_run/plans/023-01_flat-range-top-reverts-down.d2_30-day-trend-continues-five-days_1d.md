---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: a coin whose 30-day net move is large relative to its 30-day high-low range -> kept: a regime rule selects bars where the 30-bar net move over the 30-bar high-low range is at least 0.5, half the range by convention.
- Comparison: the larger its 30-day return, the further the move -> kept: the forecast is graded by the standardised 30-bar return.
- Outcome: the coin moves further in the same direction over the next 5 days -> kept: the book holds 5 bars, long after a rise and short after a fall.
- Verdict transfer: yes: the test measures this condition, this grading and this 5-day continuation directly.
Forecast: The regime detector computes NetMoveToRangeRatio over 30 bars with source high_low. - On bars where that ratio is 0.5 or more (the "trending" regime), the forecast is the 30-bar percent return, standardised against its own past 60 values (min_periods 20). - The forecast is positive after a 30-day rise and negative after a 30-day fall. - Its size grows with the size of the 30-day return, up to the cap of ±20. - On every other bar the forecast is 0 (flat).
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The Pearson correlation between the forecast and the coin's next 5-bar return minus its normal drift. - Cases are trending-regime bars with a non-zero forecast, on each window's non-overlapping 5-bar grid. - Data from all coins and windows are pooled. - The correlation's t is reported with the case count.
- Supporting check: The book's mean daily return, before costs, minus its gain from the market's own rise (the timing part) must be above 0.
- Confirm: The correlation is positive with t ≥ 2, and the timing part is above 0.
- Reject: The correlation is negative with t ≤ -2.
- Inconclusive: Either of these results is inconclusive, and so is any result on fewer than 30 independent cases: - a t between -2 and 2; - t ≥ 2 while the timing part is at or below 0.
