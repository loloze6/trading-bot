---
idea: 049-01_choppy-scaled-five-day-rise-continuation
brief: 049_scaled-five-day-moves-continue-outside-uptrends
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: in a choppy market, after a five-day rise -> adapted: "after" becomes "while" the 5-day return is positive; the code adds the choppy profile; the forecast is zero on bars with no rise.
- Comparison: the 5-day return in units of its 30-day daily-return swing -> kept: the 5-day return divided by the standard deviation of the last 30 daily returns.
- Outcome: the coin rises further over the next 3 days, more for a larger scaled rise -> kept: long, graded by the scaled rise, held 3 bars.
- Verdict transfer: yes: a long book sized by the scaled 5-day rise, held 3 days inside the choppy profile, measures exactly this claim.
Forecast: Uses `VolatilityScaledReturnComponent` with `period` 5 and `vol_period` 30. This is the 5-day return divided by the 30-day standard deviation of daily returns. The component also divides by sqrt(5), a constant factor that `standardise` removes. The value is standardised over its past 60 values (`min_periods` 20), then clipped at 0, so the forecast is long-only. It is zero when the coin did not rise over the last 5 days. It is positive after a rise and grows in proportion to the rise measured in the coin's own daily swing, capped at 20. Step 3's code keeps the book flat outside the choppy profile.
Config: 049-01_choppy-scaled-five-day-rise-continuation_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The excess 3-bar return on cases. A case is a bar with forecast > 0, taken on the non-overlapping 3-bar grid of each window. The excess return is the coin's 3-bar forward return minus the coin's mean 3-bar return over all its windows. The t is computed with cases on the same day pooled into one.
- Supporting check: The mean excess return of cases in the top half of the forecast minus that of the bottom half must be above 0.
- Confirm: The main measure's mean is positive with t ≥ 2, and the supporting check passes (top half minus bottom half > 0).
- Reject: The main measure's mean is negative with t ≤ -2.
- Inconclusive: A main t between -2 and 2, or a main t ≥ 2 with the top-minus-bottom difference ≤ 0. Fewer than 100 cases, or cases on fewer than 60 distinct days, is inconclusive whatever the result.
