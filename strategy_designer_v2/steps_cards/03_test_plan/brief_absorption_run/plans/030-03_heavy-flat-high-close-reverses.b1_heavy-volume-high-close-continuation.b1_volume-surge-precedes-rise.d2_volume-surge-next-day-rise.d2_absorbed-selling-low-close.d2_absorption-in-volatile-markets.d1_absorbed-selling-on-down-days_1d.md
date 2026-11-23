---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day with heavy volume against its prior 20-day average, a close low in its high-low range, and 20-day volatility high against its history -> adapted: the volume ratio, close location and volatility ratio are multiplied into one graded size; "high volatility" becomes a graded factor.
- Comparison: the same signal on days that closed up is refused -> kept: a regime holds only on days that closed lower, and up days are flat.
- Outcome: the coin rises over the next day, more the deeper that day's fall in 20-day volatility units -> kept: long for 1 bar, with the fall depth adding to the size.
- Verdict transfer: yes: the forecast is long only on down days and grows with each named strength, so a confirm or a reject of its next-day gains transfers to the idea.
Forecast: A regime is set to mean_reversion only on days whose close is below the prior close. Every other day is flat. On those down days the forecast is the equal-weight mean of two standardised, non-negative parts. - Part one is VolumeWeightedCloseLocationVolatilityRatioComponent (volume_period 20, vol_period 20, vol_lookback 60). It multiplies three things: how near the close is to the day's low, the day's volume over its prior 20-day mean, and the 20-day volatility over its 60-day mean. It is standardised over 80 bars. - Part two is the day's return in 20-day standard deviations, VolatilityScaledReturnComponent (period 1, vol_period 20). It is standardised over 60 bars, then negated and clipped at 0, so a deeper fall gives a larger value. The forecast is never negative. It is 0 on up days and grows continuously with heavier volume, a lower close, higher volatility and a deeper fall.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The timing gain on bars in a position, pooled over all coins and windows. On each bar it is the position held times the next-day return, minus the position held times the coin's mean daily return over all windows. The test is the ordinary t of its mean over those bars.
- Supporting check: The test takes the bars in a position and splits them into thirds by forecast. Among them, the top third's mean next-day return minus the coin's mean daily return must exceed the bottom third's, with a Welch t > 0.
- Confirm: The mean timing gain has t >= 2 over at least 300 bars in a position, and the supporting check passes.
- Reject: The mean timing gain has t <= -2 over at least 300 bars in a position.
- Inconclusive: The result is inconclusive in these cases: - t is between -2 and 2; - t >= 2 but the supporting check fails; - there are fewer than 300 bars in a position.
