---
idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a large one-day rise against the coin's 20-day standard deviation of daily returns, in a coin whose 90-day return is negative -> adapted: the 90-day return below 0 is a regime; the size of the rise is graded rather than cut at a threshold.
- Comparison: the shallower the coin's 90-day fall, the larger the fall that follows -> kept: the 90-day return is recorded on each case and set against the fall that follows it.
- Outcome: the price falls over the next 5 days -> kept: a short position held for 5 bars.
- Verdict transfer: yes: the same regime, rise, horizon and fall-depth relation are measured, so a confirm or a reject carries over to the idea.
Forecast: The forecast is active only when the coin's 90-day return is below 0. On other bars it is 0. While active, it reads the day's return divided by its 20-day standard deviation of daily returns, standardised over 60 bars. Falls are clipped to 0. The value then goes through the strongest graded dead zone the guide allows (signed_power, exponent 3, pivot 20) and is negated. The forecast is therefore 0 on down days and near 0 on ordinary up days. It is short, and grows steeply, as the rise grows to several usual daily moves, capped at -20. A second component records the 90-day return with weight 0. It does not change the forecast; it only records the fall's depth for the criterion.
Config: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: a fall of the forecast of at least 2 points, read once per non-overlapping 5-bar grid cell. For each case, take the coin's 5-day return from the signal bar's close, minus the coin's normal 5-day drift over all its windows, in the short direction. The measure is the mean of this unusual move over all cases, with its t.
- Supporting check: Across the cases, regress the short-direction unusual move on the recorded 90-day return (`fall90` `last_history_value`). The slope's t must be 2 or more: a higher (shallower) 90-day return should give a larger fall.
- Confirm: The main measure's mean is positive with t ≥ 2, and the supporting check's slope has t ≥ 2.
- Reject: The main measure's t is ≤ -2 (bounces in falling coins rise further), or the slope's t is ≤ -2 (deeper falls give larger fades).
- Inconclusive: Any other result, including a main t or slope t between -2 and 2. Fewer than 30 cases across all coins and windows is also inconclusive, whatever the t.
