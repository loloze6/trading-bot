---
idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour fall that is large against the coin's usual 24-hour move, while the bar range over those 24 hours is above its 30-day average -> adapted: "large fall" made graded (the 6-bar return in usual 6-bar moves, falls only), and range above its 30-day average kept as a while-condition regime.
- Comparison: the usual 24-hour move, the 30-day average bar range, and the coin's usual drift -> kept: the 6-bar mean absolute return over 180 bars, the 180-bar mean bar range, and the coin's mean 84-bar return.
- Outcome: the coin earns more than its usual drift over the next 14 days, more for a larger fall times range expansion, whatever its prior 30-day return -> kept: 84-bar excess return over drift, growing with the position, with no prior-trend filter.
- Verdict transfer: yes: the forecast is long only in a wider-range 24-hour fall, sized by the fall's depth in usual moves, and is judged on the 14-day excess over the coin's drift.
Forecast: The forecast is long only while the mean bar range of the last 6 bars (24h) is above its 180-bar (30-day) mean, that is while MeanBarRangeRatio(long 180, short 6) is below 1; on all other bars it is flat. In that regime it takes the 6-bar return divided by the mean absolute 6-bar return over 180 bars (the fall in usual 24h moves). This is standardised over 186 bars and negated, so a fall is positive. It is then clipped at 0, so rises give 0, and damped with signed_power (exponent 2, pivot 10). The forecast is 0 with no fall, small for a modest fall, and grows quadratically with the depth of the fall up to the +20 cap. It is never negative.
Config: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The cases are the bets: rises of the forecast of at least 2 points, read once per 84-bar grid cell. For each case, take the coin's 84-bar return from the signal bar minus the coin's normal 84-bar drift (its mean over all windows). Take the mean over all cases, before costs, with its t.
- Supporting check: The least-squares slope of the per-case excess return on the forecast at the signal bar is positive.
- Confirm: The mean excess return is positive with t >= 2 over at least 30 cases, and the slope is positive.
- Reject: The mean excess return is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a positive t of 2 or more with a slope that is not positive. So is any result with fewer than 30 non-overlapping cases across all coins and windows.
