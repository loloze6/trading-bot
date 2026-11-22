---
idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a coin whose 90-day return is negative makes a one-day rise that is large against its 20-day standard deviation of daily returns -> adapted: the 90-day fall is a regime condition held "while" it lasts; "large" is made graded by a convex dead zone on the volatility-scaled one-day rise.
- Comparison: the shallower the 90-day fall, the larger the fall that follows -> kept: each case's 90-day return is recorded and the case's outcome is regressed on it.
- Outcome: a fall over the next 5 days -> kept: a short held 5 bars.
- Verdict transfer: yes: the plan measures the falling-market condition, the bounce in usual moves, the 5-day fall and its link to the depth of the fall as the idea states them.
Forecast: The forecast is active only while the coin's 90-day close-to-close return is below 0. Outside that regime it is flat. Inside it, it reads today's one-day return divided by the 20-day standard deviation of daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). This value is standardised over 60 bars and clipped at 0, so down days give 0. It then passes through signed_power (exponent 3, pivot 20), so ordinary up days stay near 0 and only bounces of several usual moves give a sizeable value. That value is negated. The forecast is therefore 0 or negative and never positive. The short grows smoothly with the size of the bounce, up to -20 for the largest. A second component, the 90-day return, has weight 0. It does not change the forecast and is there only so that each case's depth of fall is recorded for the comparison.
Config: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: a fall of the forecast of at least 2 points, read once per non-overlapping 5-bar grid cell of each window. For each case, take the coin's 5-day return from the signal bar's close. Subtract the coin's normal 5-day drift, measured over all its windows. Flip the sign so that a fall counts as positive. The main measure is the mean of this unusual move over the cases, with the t of the mean.
- Supporting check: Across the cases, regress the unusual move (short direction) on the case's 90-day return (depth90 last_history_value). The slope must be positive, meaning shallower falls are followed by larger falls, with a t of 2 or more.
- Confirm: The idea is confirmed only when both hold: - the mean unusual move is positive with t ≥ 2; - the depth slope is positive with t ≥ 2.
- Reject: The idea is rejected if either holds: - the mean unusual move is negative with t ≤ -2, meaning bounces in falling coins keep rising beyond drift; - the depth slope has t ≤ -2, meaning deeper falls are followed by the larger fades.
- Inconclusive: Any other result is inconclusive. This includes a mean t between -2 and 2, and a confirmed main measure with a slope t between -2 and 2. The test needs at least 30 cases in total, from at least 3 coins; with fewer, it is inconclusive.
