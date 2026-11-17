---
idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: days the 14-day RSI has stayed below 50 without a break, up to the close -> kept: RsiMidlineAgeComponent (period 14) gives the run length below 50 in daily bars.
- Comparison: longer stretches against shorter ones (the longer, the lower) -> kept: the short position grows with the run length.
- Outcome: lower return over the next 7 days -> kept: 7-day forward return, read as short when the stretch is long.
- Verdict transfer: yes: the forecast is the stretch length itself, and the outcome is the 7-day return.
Forecast: The forecast uses RsiMidlineAgeComponent with RSI period 14, max_bars 60 and rsi_window 100. Its raw value is +n while RSI has been above 50 for n days, and -n while it has been below 50 for n days. - It is standardised against its own past 160 values (min_periods 40). - It is then clipped at a maximum of 0, so only the below-50 side remains. - It is zero while RSI is above 50. - It is negative (short) while RSI is below 50, about -0.17 on the first day below 50. It grows more negative each further day the stretch lasts and reaches the cap of -20 once the run is long enough, at the latest at the 60-day cap. - It returns to 0 when RSI crosses back above 50.
Config: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: On each window's non-overlapping 7-bar grid, take the bars with forecast < 0 and regress the excess 7-day return on the run length (-last_history_value). The excess return is close[t+7]/close[t]-1 minus that coin's mean 7-day return over all windows. Report the t of the slope, pooled over the coins.
- Supporting check: On the same grid bars, the mean of (forecast/10 × excess 7-day return) is above 0. This means the short side gained against holding the coin.
- Confirm: The slope's t is ≤ -2 and the supporting check passes.
- Reject: The slope's t is ≥ +2, meaning longer stretches are followed by higher excess returns.
- Inconclusive: Any slope t between -2 and +2, or a confirming slope whose supporting check fails. At least 100 grid cases with forecast < 0 are required; fewer is inconclusive.
