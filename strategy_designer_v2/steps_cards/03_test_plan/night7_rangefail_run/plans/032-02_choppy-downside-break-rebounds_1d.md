---
idea: 032-02_choppy-downside-break-rebounds
brief: 032_choppy-market-breakouts-fail
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a choppy market, the daily close is below the lowest low of its prior 20 days -> kept: the choppy profile is added by code, and a regime rule fires only when the close is below the prior 20-day low.
- Comparison: the further the close sits below that low, the larger the rise -> kept: the forecast is graded by the close's percent depth below the prior 20-day low.
- Outcome: the price rises over the next 5 days -> kept: a long position held for 5 daily bars.
- Verdict transfer: yes: the test holds a long position only on closes below the prior 20-day low in choppy markets, and sizes it by the depth of the break, which is exactly what the idea claims.
Forecast: The forecast uses `DistanceFromHighComponent` with `period` 20, `source` "high", `exclude_current` 1, `extreme` "low" and `form` "percent". It gives the close's percent distance from the lowest low of the prior 20 days, which is negative below that low. A regime rule selects `mean_reversion` only when this distance is below 0, so the close has broken the prior 20-day low. Every other bar is flat. Inside the regime, the value is standardised (window 60, min_periods 20), negated, and clipped at 0. The forecast is therefore 0 at the edge of the low and grows continuously with the depth of the break. It is long only and never negative. The code adds the choppy profile on top, so the book is flat outside choppy markets.
Config: 032-02_choppy-downside-break-rebounds_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual move over the cases. A case is a bet, read once per 5-bar grid cell. The unusual move is the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows. Its t has the cases of one day taken together.
- Supporting check: The least-squares slope of the per-case unusual move on the forecast at the signal bar must be above 0, so that deeper breaks give larger rises.
- Confirm: The idea is confirmed only when both hold: - the mean unusual move is above 0 with t ≥ 2; - the slope on the forecast is positive.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with a slope of 0 or below is also inconclusive. Fewer than 30 cases, or cases falling on fewer than 30 distinct days, can neither confirm nor reject.
