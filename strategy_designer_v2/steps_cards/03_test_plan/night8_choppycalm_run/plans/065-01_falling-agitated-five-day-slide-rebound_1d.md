---
idea: 065-01_falling-agitated-five-day-slide-rebound
brief: 065_agitated-downtrend-slide-depth-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a coin's fall over the past five days, in a falling, agitated market -> kept: 5-bar return, long only while it is negative; the profile is added by code.
- Comparison: none -> kept
- Outcome: the deeper the five-day fall, the larger the rise over the next day -> kept: next-bar return, graded by depth.
- Verdict transfer: yes: the forecast is the five-day fall depth inside the profile, and it is judged on the next day's rise.
Forecast: One `PriceEvolutionComponent` with a 5-bar period gives the 5-day return in percent. It is standardised over its last 60 values (20 at least), then negated, then clipped at 0. The forecast is 0 when the coin rose or was flat over the five days. It is positive after a five-day fall and grows in proportion to the fall's depth against the coin's usual five-day move size, up to the cap of 20. It is never short. Outside the falling, agitated profile, code keeps the book flat.
Config: 065-01_falling-agitated-five-day-slide-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: The cases are bars inside the profile with forecast above 0, one per bar, with no overlap. On these cases, regress the coin's next-day return minus its mean daily return over all windows on the forecast (`post_pipeline_value` of slide5). Report the slope and its t, with the cases of one day taken together.
- Supporting check: The forecast-weighted mean of the cases' next-day excess return is above 0.
- Confirm: The slope is positive with t ≥ 2, and the forecast-weighted mean excess return is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: A slope t between -2 and 2, or t ≥ 2 with a weighted mean at or below 0. Fewer than 200 cases, or cases on fewer than 50 distinct days, is also inconclusive.
