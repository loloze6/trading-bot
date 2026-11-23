---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day's fall, measured in units of the coin's own 20-day daily volatility, larger the deeper -> kept
- Comparison: ordinary or rising days, where the buy is refused -> adapted: graded, zero after rising days and small after shallow falls.
- Outcome: the coin rises over the next day, more after deeper falls -> kept
- Verdict transfer: yes: the forecast is the idea's own volatility-scaled fall, held one day, judged on the next day's move.
Forecast: One indicator, the day's close-to-close return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised against its last 60 values (min_periods 20), then negated so that a fall reads positive, then clipped at 0. The result is zero after rising or flat days. After a fall it is positive and grows linearly with the fall's depth in usual moves: a fall of one usual move gives about +10, and the value is capped at +20. It never goes below zero, so the book is long only. No regime is used.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The forecast-weighted mean of the next-day excess return on bars with forecast > 0, with its t. The excess return is close[t+1]/close[t] − 1 minus the coin's mean daily return over all its windows. Every bar inside a window is a non-overlapping case at horizon 1.
- Supporting check: On bars with forecast > 0, the Spearman correlation between the forecast and the next-day excess return is above 0.
- Confirm: The weighted mean excess return is positive with t ≥ 2, and the supporting check passes.
- Reject: The weighted mean excess return is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2, a positive t ≥ 2 that fails the check, or fewer than 200 bars with forecast > 0 across all coins and windows.
