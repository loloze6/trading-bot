---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bc0cb550291c
---
Fidelity:
- Situation: a day's fall, heavier when volume is high against its prior 20-day mean -> kept: `FallVolumeVolatilityWeightedComponent`, fall in percent x volume[t] / mean of the prior 20 days.
- Comparison: 20-day volatility high against 4-month volatility, more so the higher -> adapted: the "while high" condition is made graded, by multiplying by the 20/120-bar volatility ratio.
- Outcome: the coin rises over the next day -> kept: long, horizon 1 bar.
- Verdict transfer: yes: the forecast is exactly the idea's product of fall, volume ratio and volatility ratio, so its next-day result answers the idea.
Forecast: One indicator, `FallVolumeVolatilityWeightedComponent` (volume_period 20, vol_period 20, base_vol_period 120). It multiplies three things: the day's fall in percent, the day's volume over its prior 20-day mean, and the 20-day over the 120-day return volatility. The product is standardised against its own past 121 values (min_periods 30). The forecast is 0 on up days and flat days, so it is never short. It is positive on down days and grows with the size of the fall, the volume surge and the volatility ratio. On calm-market days the low volatility ratio keeps it small.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The forecast-weighted mean of the next-day excess return. A case is a bar with forecast > 0, pooled over coins and windows. The excess return is close[t+1]/close[t] − 1 minus the coin's mean daily return over all its windows. The t-statistic is taken over the cases.
- Supporting check: The mean excess return of the top-third forecast cases minus that of the bottom-third cases is above 0 (the relation grows with size).
- Confirm: The main measure is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The main measure is below 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2, or a confirming t with a failed check. A test needs at least 300 cases with forecast > 0; with fewer the result is inconclusive.
