---
idea: 032-01_monthly-low-break-cascade
brief: 032_monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a falling, agitated market, a daily close below the lowest close of the previous 30 days -> adapted: the profile is added by code, and the break below the prior 30-day closing low is a regime condition (flat on every other bar)
- Comparison: the further the close sits below that prior low, the larger the fall -> kept: the short position is graded by the close's percent depth below the prior 30-day low
- Outcome: price keeps falling over the next 3 days -> kept: 3-bar short hold, judged against the coin's normal drift
- Verdict transfer: yes: the test bets only on fresh 30-day closing lows, sized by their depth, and judges the following 3-day move.
Forecast: Only on bars where the close is below the lowest close of the prior 30 bars (bar t excluded) is the book short; on every other bar it is flat. The measure is DistanceFromHighComponent (`extreme` "low", `period` 30, `source` "close", `exclude_current` 1, `form` "percent"), the close's percent distance from the prior 30-day low. It is standardised over its past 60 values (`min_periods` 20) and clipped at 0. Inside the regime the forecast is therefore negative, and its size grows with the depth of the break.
Config: 032-01_monthly-low-break-cascade_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Over the cases (short bets on the 3-bar grid), the coin's 3-bar return from the signal bar's close, minus the coin's normal 3-bar drift, read in the short direction (the unusual move). Its t uses cases pooled by day.
- Supporting check: Over the same cases, the slope of the 3-bar return on the forecast (`post_pipeline_value`) is positive with t ≥ 1, meaning deeper breaks are followed by larger falls.
- Confirm: The mean unusual move in the short direction is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move in the short direction is below 0 with t ≤ -2, meaning the coin rebounds after a fresh monthly low.
- Inconclusive: Any t between -2 and 2, or a confirm-side main measure whose supporting check fails. The test also needs at least 30 cases on at least 30 distinct days; with fewer it is inconclusive.
