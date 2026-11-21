---
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two days (12 bars), after the coin fell over the past 7 days (42 bars) -> kept: a regime rule requires the close above the prior 12-bar high and a negative 42-bar return; "after" becomes "on that same bar".
- Comparison: the deeper the past week's fall, the larger the decline -> kept: the short is sized by the 42-bar fall, standardised.
- Outcome: the coin falls over the next three days (18 bars) -> kept: a short held 18 bars.
- Verdict transfer: yes: the test shorts exactly these breakout bars, sized by the week's fall, over three days, so its result is the idea's result.
Forecast: The regime detector selects `trending` only on a bar where both conditions hold: - the close is above the highest high of the previous 12 bars (DistanceFromHigh, period 12, source high, current bar excluded, above 0); - the 42-bar price change is below 0. On every other bar the forecast is 0. On a selected bar the forecast is the 42-bar price change, standardised over its last 60 values (min_periods 20). It is always negative there, so the position is always short. It grows in size with the depth of the week's fall, about -10 for a fall of usual size and up to -20 for a deep one.
Config: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are short bets (a fall of the forecast of at least 2 points from its level since its last bet), read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the case bar's close minus the coin's mean 18-bar return over all its windows, with the sign flipped (positive when the coin falls more than usual). Measure the mean over all cases with its t.
- Supporting check: Split the cases at the median of |forecast|. The deeper-fall half's mean drift-adjusted short return minus the shallower half's must be above 0.
- Confirm: The mean drift-adjusted short return has t ≥ 2 with at least 30 cases, and the supporting check is above 0.
- Reject: The mean drift-adjusted short return has t ≤ -2 with at least 30 cases (the coin rises more than usual after these breakouts).
- Inconclusive: Any of these is inconclusive: - t between -2 and 2; - t ≥ 2 but the deeper half is not ahead of the shallower half; - fewer than 30 cases.
