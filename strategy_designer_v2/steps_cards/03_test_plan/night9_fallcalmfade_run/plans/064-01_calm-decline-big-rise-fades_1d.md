---
idea: 064-01_calm-decline-big-rise-fades
brief: 064_falling-calm-scaled-rallies-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling, calm market, a one-day rise that is large against the past 20 days' daily swing -> adapted: the profile is added by code; "large" is a regime condition at the usual 2 swings (20-day std of daily returns), graded inside it by the rise in swings.
- Comparison: the rise measured in units of its own past-20-day daily swing -> kept
- Outcome: the price falls over the next three days, more the larger the rise -> kept
- Verdict transfer: yes: the test bets short only on large scaled rise days in falling calm markets, sized by the rise, held 3 days, and is judged on the fall that follows and on how it grows with size.
Forecast: The forecast uses one quantity: today's one-day return divided by the standard deviation of the last 20 daily returns, which is the rise in swings. A bar enters the regime only when that rise is 2 swings or more, inside the falling calm profile. On every other bar the forecast is 0. Inside the regime the rise is standardised against its own past 60 values and negated, so the forecast is always short. The standardise target is 4, so with an average absolute value of about 0.8 swings a 2-swing rise gives about -10 and a rise of 4 swings or more reaches the -20 cap. The short grows continuously with the size of the rise.
Config: 064-01_calm-decline-big-rise-fades_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: On case bars (regime mean_reversion, forecast below 0, read once per 3-bar grid cell), the coin's 3-bar return close[t+3]/close[t]-1 minus its normal 3-bar drift over all windows, taken in the short direction. The measure is its mean and its t, with the cases of one day pooled.
- Supporting check: Across the cases, the Pearson correlation between abs(forecast) and the short-direction excess 3-bar return is positive.
- Confirm: The mean short-direction excess return is above 0 with t >= 2 on at least 30 cases, and the correlation is above 0.
- Reject: The mean short-direction excess return is below 0 with t <= -2 on at least 30 cases. In that case the price rises after large scaled up days.
- Inconclusive: Any t between -2 and 2, or a confirming t with a correlation at or below 0, or fewer than 30 cases.
