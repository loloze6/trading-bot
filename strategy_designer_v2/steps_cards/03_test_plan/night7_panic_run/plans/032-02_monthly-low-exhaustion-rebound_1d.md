---
idea: 032-02_monthly-low-exhaustion-rebound
brief: 032_monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a coin closes below the lowest close of its previous 30 days, in a falling, agitated market -> kept: the profile is added by code, and the break below the prior 30-day closing low is a regime condition.
- Comparison: how far the close sits below that prior 30-day low -> kept: the depth in percent of the prior low grades the long.
- Outcome: price rebounds over the next 3 days, more for deeper breaks -> adapted: "after the break" becomes "while the break holds", and each bet is held for 3 bars.
- Verdict transfer: yes: the test measures the 3-day move after graded breaks of the prior 30-day low inside the profile, which is exactly the idea's claim.
Forecast: The forecast uses `DistanceFromHighComponent` with `period` 30, `source` "close", `exclude_current` 1, `extreme` "low" and `form` "percent". It gives the close's percent distance from the lowest close of the prior 30 days. The detector sends a bar to `mean_reversion` only when that distance is below 0, a fresh 30-day closing low. Every other bar goes to `unknown`, which is flat. Inside the regime the distance is standardised against its past 60 values, clipped at a maximum of 0 and negated. The forecast is therefore long only. It is zero at the prior low and grows linearly with the close's depth below it, capped at 20. Outside the regime, and outside the falling agitated profile (added by code), it is 0.
Config: 032-02_monthly-low-exhaustion-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases: each case is a forecast rise of at least 2 points, read once per 3-bar grid cell. For each case, take the coin's 3-day return from the signal bar's close, minus its normal 3-day drift (holding the coin, mean over all windows). Report its t, with the cases of one day pooled, before costs.
- Supporting check: Split the cases at the median of `depth.last_history_value`. The mean unusual move of the deeper half minus that of the shallower half must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2, meaning the coin keeps falling after the break.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 when the deeper half does not beat the shallower half. So is any result with fewer than 30 distinct case days across coins and windows.
