---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's 1-hour return in the first hour after the 00:00 UTC settlement, against its 24-hour volatility -> adapted: a regime selects the bar 00:00–01:00, and its return is divided by the 24-bar standard deviation of hourly returns, graded.
- Comparison: the 24-hour volatility against its 30-day volatility -> kept: it enters as the factor s24(t) / mean of s24 over the last 720 bars, so the size grows with the ratio.
- Outcome: the next 24 hours run opposite to that hour's return -> kept: the position is a fade held 24 bars.
- Verdict transfer: yes: the forecast is the settlement-hour return in 24h-volatility units times the volatility ratio, faded over 24 hours, which is the idea as stated.
Forecast: The forecast is non-zero only at the close of the bar that starts at 00:00 UTC. A regime rule on HourOfDayComponent fires when the coming bar starts at hour 1. On that bar the forecast reads VolatilityScaledReturnComponent (period 1, vol_period 24, vol_lookback 720). This is the bar's return divided by the mean, over the last 720 bars, of the 24-bar return standard deviation. That equals the return in 24h-volatility units times the ratio of 24h volatility to its 30-day average. The value is standardised over its past 500 hourly values (target 10, cap 20) and then negated. So a large rise in the settlement hour gives a short, and a large fall gives a long. The size grows with the move's size in usual hourly moves and with how raised the 24h volatility is against the month. It is near 0 when the hour barely moves. On every other hour the regime is null and the forecast is 0. The bet is kept for 24 bars by the holding period.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are the bars where the regime is mean_reversion and the forecast is non-zero: one per coin per day, 24 bars apart, so they do not overlap. For each case, take the coin's return from that close over 24 bars, inside the window. Subtract the coin's mean 24-bar return over all its windows (holding the coin). Then estimate the pooled slope, and its t, of this excess return on the forecast, before costs.
- Supporting check: Split the cases at the median of the volatility ratio s24(t) / mean(s24 over 720 bars), recomputed from closes. The fade gain per case is sign(forecast) × excess return × |forecast| / 10. Its mean in the high-ratio half minus the low-ratio half must be above 0.
- Confirm: The slope is positive with t ≥ 2 over at least 1000 cases, and the supporting check's difference is above 0.
- Reject: The slope is negative with t ≤ -2 over at least 1000 cases: settlement-hour moves are followed by continuation, not reversal.
- Inconclusive: Either a slope t between -2 and 2, or t ≥ 2 with the high-ratio half not above the low-ratio half. Also inconclusive with fewer than 1000 cases.
