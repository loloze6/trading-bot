---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a day of unusually large fall, measured in units of its own 20-day daily volatility -> adapted: "unusually large" has no number, so it takes the 2-usual-move convention as a regime; inside it the position grows with the depth of the fall.
- Comparison: the fall against the coin's 20-day volatility; no buy after ordinary or rising days -> kept: return over 20-day std, and flat outside the regime.
- Outcome: the coin rises over the next day, more the deeper the fall -> kept: a long position held 1 bar.
- Verdict transfer: yes: the test holds long only after falls of 2 or more usual moves, sized by depth, and reads the next day's rise.
Forecast: VolatilityScaledReturnComponent (period 1, vol_period 20) gives the day's return in units of its 20-day volatility. When it is -2 or below, the regime is mean_reversion; on every other bar the forecast is 0. Inside the regime, the same value is standardised (window 60, min_periods 20), negated and clipped at 0, so the forecast is a long that grows with the depth of the fall. Standardise uses target 5 so that a 2-usual-move fall gives about 13 and the cap of 20 is reached only near 3 usual moves. At the default target of 10, every regime bar would sit at the cap and the position would be on/off.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On the case bars (regime mean_reversion with forecast > 0), the coin's next-day return close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. Report the mean and its t, with cases on the same day taken together.
- Supporting check: Split the cases at their median forecast. The mean excess next-day return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess next-day return is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean excess next-day return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. At least 30 cases (case days) are required; with fewer, the result is inconclusive.
