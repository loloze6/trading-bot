---
idea: 038-01_agitated-fall-next-day-rebound
brief: 038_agitated-decline-big-falls-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall in a falling, agitated market -> adapted: the falling agitated profile is added by code as the regime; inside it the fall size is graded, 0 on up days
- Comparison: none -> kept
- Outcome: the next day's rise grows with the size of the fall -> kept
- Verdict transfer: yes: the forecast is the day's percent fall inside the profile, so a next-day return that grows with it confirms the idea, and one that shrinks with it rejects it.
Forecast: The forecast is the one-day close-to-close return in percent (`PriceEvolutionOnPeriodComponent`, `comparison_period` 1). It is standardised against its own last 60 values (`min_periods` 20), then negated and clipped at 0. It is positive only on down days, and it grows linearly with the day's fall measured against the coin's usual daily move size, up to the cap of 20. It is 0 on up days and flat days, and never short (the brief is long only). The code keeps the book flat outside the falling agitated profile.
Config: 038-01_agitated-fall-next-day-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The cases are the bars with forecast > 0 (down days in the profile). On those cases, take the slope of the next-day return minus the coin's mean daily return over all windows, regressed on the forecast. Its t uses standard errors clustered by day, before costs.
- Supporting check: On those cases, the forecast-weighted mean of the next-day excess return is above 0.
- Confirm: The slope is positive with t ≥ 2, and the weighted mean excess return is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2. A confirmed slope whose weighted mean is not above 0 is also inconclusive. So is a test with fewer than 100 cases on at least 60 distinct days.
