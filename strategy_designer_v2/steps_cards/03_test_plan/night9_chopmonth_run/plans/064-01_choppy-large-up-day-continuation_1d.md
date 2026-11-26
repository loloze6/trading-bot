---
idea: 064-01_choppy-large-up-day-continuation
brief: 064_choppy-market-up-days-carry-one-way
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a choppy coin's one-day return is a large rise against its 30-day daily swing -> adapted: "large" is a regime at 2 swings or more (no number in the idea or brief, so the most common convention), graded by size inside it; the choppy profile is added by code.
- Comparison: the rise against the standard deviation of daily returns over the past 30 days -> kept
- Outcome: keeps rising over the next 5 days, more the larger the jump -> kept: each bet is held 5 bars and sized by the jump.
- Verdict transfer: yes: the test bets long only on large scaled up days, sizes by their scale and holds for the 5 days the idea names.
Forecast: The detector computes the day's return divided by the standard deviation of the last 30 daily returns (`VolatilityScaledReturnComponent`, `period` 1, `vol_period` 30). On bars where this is 2 or more, the regime is `trending`; every other bar is `unknown`, which is flat. Inside the regime, the forecast is that same scaled return. It is standardised over its past 60 values with target 3, so the forecast grows with the jump rather than sitting at the cap. A 2-swing day gives about 8, and a 5-swing day reaches the cap of 20. It is clipped at 0, so it is long only. The forecast is zero outside large up days and outside the choppy profile.
Config: 064-01_choppy-large-up-day-continuation_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: For each case (a long bet, read once per 5-bar grid cell), the coin's 5-bar return from the signal bar's close minus the coin's normal 5-bar drift, divided by its usual 5-bar move. This is averaged over cases, with the t computed on cases grouped by day.
- Supporting check: The mean unusual move of cases whose forecast is above the cases' median forecast, minus that of cases at or below it, is above 0.
- Confirm: The mean strength is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean strength is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming main measure whose supporting check fails. At least 30 cases on at least 30 distinct days are required; fewer is inconclusive.
