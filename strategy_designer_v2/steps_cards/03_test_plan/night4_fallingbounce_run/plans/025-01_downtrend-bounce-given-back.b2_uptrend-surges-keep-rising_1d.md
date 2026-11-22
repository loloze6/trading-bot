---
idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a one-day rise large relative to the 20-day standard deviation of daily returns, in a coin whose 90-day return is not negative -> adapted: "large" is made graded, as the one-day return in 20-day standard deviations, kept only on its positive side; "90-day return not negative" is kept as a regime rule.
- Comparison: the rise is judged against the usual daily move, the 20-day standard deviation -> kept
- Outcome: a further rise over the next 5 days, larger after larger rises -> kept: the horizon is 5 bars, and the position grows with the rise.
- Verdict transfer: yes: the forecast is long exactly in proportion to the scaled up-day, only when the 90-day return is at or above 0, and it is judged on the 5-day move that follows.
Forecast: The regime is active only when the 90-day percent return is 0 or more (PriceEvolutionOnPeriodComponent, comparison_period 90, rule gte 0); on other bars the forecast is flat. In that regime the forecast is today's one-day return divided by the 20-day standard deviation of daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). The steps are: - It is standardised against its past 60 values. - It is clipped at 0, so down days give 0 and the forecast is long only. - A signed_power with exponent 3 and pivot 20 is applied, so that ordinary up-days stay near 0. A standardised 10 gives 2.5, 15 gives about 8.4, and 20 stays 20. The forecast is never negative. It is 0 on down days and in coins with a negative 90-day return, and it grows steeply with the size of the up-day in usual moves.
Config: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on the cells whose forecast is above 0. Regress the coin's 5-bar forward return, minus that coin's mean 5-bar return over all windows, on the forecast. Report the slope and its t, all coins pooled.
- Supporting check: On the cells with forecast 5 or more, the mean excess 5-bar return (forward return minus the coin's mean 5-bar return) is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes, with at least 30 grid cells with forecast above 0.
- Reject: The slope's t is -2 or less, with at least 30 grid cells with forecast above 0.
- Inconclusive: Either of these is inconclusive, not a confirm or a reject: - a slope t between -2 and 2; - a slope t of 2 or more with the check failing. The test is also inconclusive with fewer than 30 grid cells with forecast above 0.
