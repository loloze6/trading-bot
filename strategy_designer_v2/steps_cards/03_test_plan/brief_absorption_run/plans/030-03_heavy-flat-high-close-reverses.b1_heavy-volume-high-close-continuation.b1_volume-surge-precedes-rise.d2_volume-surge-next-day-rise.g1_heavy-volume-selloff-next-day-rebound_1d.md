---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day's fall on volume heavy against the prior 20 days, with 20-day volatility -> kept: a down day with volume at or above its prior 20-day mean selects the regime, and fall size, volume ratio and 20-day volatility each grade the position inside it.
- Comparison: the day's volume against its own prior 20-day average volume -> kept
- Outcome: the coin rises over the next day, more with a bigger fall, heavier volume and higher volatility -> kept
- Verdict transfer: yes: the forecast buys only after heavy-volume falls, grows with each named factor and is held one day, so its next-day results settle the idea.
Forecast: The forecast is zero except on a bar whose one-day return is below 0 and whose volume is at least its mean over the 20 prior days (bar t excluded). On those bars it is the equal-weight mean of three parts, each standardised over 60 bars (min_periods 20): - the day's fall: the 1-bar percent return, negated and clipped at 0; - the volume ratio: volume[t] over the mean of the prior 20 volumes; - the 20-day volatility: the standard deviation of 20 daily returns. Each part sits near 10 at its usual size and grows above that as the fall, the volume surge or the volatility grows. The forecast is therefore long, never negative, about 10 on an ordinary heavy-volume down day, and up to 20 on a deep, very heavy fall in a volatile market. It is flat on up days and on light-volume days.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the coin's next-day return close[t+1]/close[t]-1 minus that coin's mean daily return over all its windows. This is pooled over coins and windows, with each bar one case, and judged by the ordinary t of the mean.
- Supporting check: Across those same bars, the slope of next-day excess return on the forecast (least squares) must be positive with t ≥ 1.
- Confirm: The mean next-day excess return is above 0 with t ≥ 2, and the slope check passes.
- Reject: The mean next-day excess return is below 0 with t ≤ -2.
- Inconclusive: Any other result is inconclusive, including t between -2 and 2, or t ≥ 2 with a slope t below 1. At least 200 active bars are needed in total; with fewer, the test is inconclusive.
