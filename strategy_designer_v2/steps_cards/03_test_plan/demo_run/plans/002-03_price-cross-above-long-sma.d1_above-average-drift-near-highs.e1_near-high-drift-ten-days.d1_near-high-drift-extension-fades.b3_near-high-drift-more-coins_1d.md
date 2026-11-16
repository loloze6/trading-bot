---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average, close high in its 20-day close range, 30-day return extended -> adapted: the 200-day condition is kept as a regime; the "extended" threshold is made graded with a cubic dead zone on the 30-day return.
- Comparison: higher versus lower range position, and larger versus smaller extended 30-day return -> kept: both are measured as graded slopes.
- Outcome: larger rise over the next 10 days, smaller when the run is extended -> kept: 10-day forward return against the coin's average.
- Verdict transfer: yes: the forecast is the idea's range position minus its graded extension, used only above the 200-day average, and it is judged on the idea's own 10-day horizon.
Forecast: The forecast is active only while the close is at or above its 200-day SMA. That condition is a regime rule on `MovingAverageDistanceComponent` (sma, 200) at 0 or more; on every other bar the forecast is flat. In that regime the forecast is the equal-weight mean of two parts: - Range position. The close's position in its 20-day close range (`DonchianBreakoutComponent`, period 20), standardised over 60 bars. It is positive in the upper half of the range and grows towards the 20-day high. It is negative in the lower half. - Extension penalty. The 30-day return (`PriceEvolutionComponent`, period 30) is standardised over 60 bars and clipped at 0. It then goes through `signed_power` with exponent 3 and pivot 20, and is negated. It is near 0 unless the 30-day run is large compared with its own past: a value of 10 gives -2.5, and 20 gives -20. The forecast therefore grows as the close nears its 20-day high. It is cut back, and can turn short, as the 30-day run becomes extended. It is zero at mid-range with no extension.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The sample is the trending-regime bars on a non-overlapping 10-bar grid in each window, pooled over coins and windows. The excess return is the coin's 10-bar forward return minus that coin's mean 10-bar return over all its windows. Regress the excess return on the forecast and take the slope and its t.
- Supporting check: Take the grid bars where `ext30` `post_pipeline_value` is at or below -5 (an extended run). On those bars, the slope of the excess 10-bar return on `ext30` `last_history_value` (the 30-day return) must be negative.
- Confirm: The main slope's t is at least +2, with at least 100 independent cases, and the supporting check gives a negative slope on at least 30 extended cases.
- Reject: The main slope's t is -2 or less, with at least 100 independent cases.
- Inconclusive: The idea is inconclusive in three cases: the main t is between -2 and +2; the main t is at least +2 but the check fails or has fewer than 30 extended cases; or there are fewer than 100 grid cases in the trending regime.
