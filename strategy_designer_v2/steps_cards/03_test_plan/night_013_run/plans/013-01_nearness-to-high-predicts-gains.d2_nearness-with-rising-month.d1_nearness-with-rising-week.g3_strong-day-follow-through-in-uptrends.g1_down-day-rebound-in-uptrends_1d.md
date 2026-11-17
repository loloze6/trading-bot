---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the latest one-day fall relative to the coin's 30-day daily volatility -> adapted: graded as the vol-scaled 1-day return, negated and kept only on down days.
- Comparison: larger falls against smaller ones, only while the 30-day return is positive -> kept: a regime on the 30-day return above zero; the position grows with fall size.
- Outcome: a higher return over the next 1 day -> kept: next-bar return on daily bars.
- Verdict transfer: yes: the test measures the stated relation, under the stated condition, at the stated 1-day horizon.
Forecast: The 30-day return (PriceEvolutionOnPeriod, 30 bars) is checked on each bar. While it is above zero, the bar is "trending" and the forecast is active. Otherwise the forecast is 0. In the active regime, the forecast comes from the 1-day return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturn, period 1, vol_period 30). That value is standardised over its past 60 values, negated, and clipped at 0. So the forecast is 0 on up days and on flat days, and on down days it is a long position. That position grows linearly with the size of the fall in usual-move units, up to a cap of 20. The forecast is never negative.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars where regime is trending and forecast > 0, pooled over all coins and windows. On those bars, compute each coin's next-1-bar return minus that coin's mean daily return over all windows. Regress this excess return on the forecast and read the t of the slope.
- Supporting check: On the same bars, take the forecast-weighted mean of the excess next-1-bar return. It must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. A positive slope with t ≥ 2 but a weighted mean excess return ≤ 0 is also inconclusive. So is any result from fewer than 100 qualifying bars in total.
