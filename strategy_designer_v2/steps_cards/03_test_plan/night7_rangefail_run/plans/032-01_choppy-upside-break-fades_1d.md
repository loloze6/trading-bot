---
idea: 032-01_choppy-upside-break-fades
brief: 032_choppy-market-breakouts-fail
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a choppy market, the daily close is above the highest high of the prior 20 days -> kept: the choppy profile is added by code, and a regime rule fires when the close is above the prior 20-day high (DistanceFromHigh above 0).
- Comparison: the further the close sits above that high, the larger the fall -> kept: the short position is graded by the close's percent distance above the prior 20-day high.
- Outcome: the price falls over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes: the test shorts exactly the stated breaks, sized by the overshoot, over the stated 5 days, so a confirm or a reject transfers to the idea.
Forecast: The forecast is built from DistanceFromHighComponent with period 20, source "high", exclude_current 1 and form "percent". It gives (close − highest high of the 20 prior days) / that high × 100. A regime rule selects `mean_reversion` only on bars where this value is above 0, that is, when the close is above the prior 20-day high. On every other bar the forecast is 0 and the book is flat. Inside the regime, the same distance is standardised against its own past 60 values (mean absolute size, 20 values minimum). It is then clipped at 0 and negated. So the forecast is negative (short) and grows in size with the overshoot. It is near 0 for a close just above the high and larger for a bigger break, capped at −20. It is never positive. The code adds the choppy profile, so the book is flat outside choppy markets.
Config: 032-01_choppy-upside-break-fades_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move of the cases in the short direction. A case is a short bet read once per 5-bar grid cell. Its unusual move is the negative of (the coin's 5-day return from the signal bar's close minus the coin's normal 5-day drift over all windows). The measure is the mean over the cases, with its t computed with cases clustered by day.
- Supporting check: Across cases, the least-squares slope of that unusual move on the case's absolute forecast (its overshoot size) is above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the slope check is above 0.
- Reject: The mean unusual move is below 0 with t ≤ −2 (the breaks keep rising beyond the coin's drift).
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with a slope at or below 0. Fewer than 30 cases, or cases on fewer than 30 distinct days, is inconclusive whatever the t.
