---
idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a large one-day fall made on heavy volume compared with its 60-day average volume -> adapted: the 60-day average volume (heavy is 1.5x, by convention) and a down day are a regime condition; "large fall" becomes a position graded by the fall's size.
- Comparison: the heavier that day's volume, the larger the rebound -> kept: the day's volume ratio is recorded and the rebound is compared across it.
- Outcome: the fall is partly undone over the next 1 day, so the price rises -> kept: the next 1-bar return, long.
- Verdict transfer: yes: the test measures the idea's own fall, volume ratio and next-day rebound, and only the size threshold is made graded.
Forecast: The forecast is active only when two things hold. Today's volume must be at least 1.5 times its 60-day average (VolumeRatio, period 60), and today's close must be below yesterday's. On those bars it is long. Its size is the day's fall measured in the coin's usual daily moves (VolatilityScaledReturn, period 1, vol_period 20). That fall is standardised over its past 60 values, negated so that falls are positive, and clipped at 0. It then passes through signed_power with exponent 3: a small fall gives almost nothing, and a fall twice the usual size reaches the +20 cap. On every other bar the forecast is 0, and it never goes short. The volume ratio is carried with weight 0, so it is recorded but does not change the size.
Config: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, pooled over coins and windows, take the next-bar return minus the coin's mean daily return over all windows (the excess return). Measure the forecast-weighted mean of this excess return, with the ordinary t of (forecast/10 x excess return).
- Supporting check: Among active bars, compare the mean excess next-bar return of the half with the higher recorded volume ratio (debug_info.components.vol.last_history_value) against the lower half, as a Welch t of high minus low.
- Confirm: The weighted mean excess return is > 0 with t ≥ 2, and the high-volume half minus the low-volume half is > 0.
- Reject: The main measure's t ≤ -2, or the main measure confirms but the high-minus-low volume difference has t ≤ -2.
- Inconclusive: Any result between those, including a main t between -2 and 2, or a confirmed main measure whose volume difference has t between -2 and 0. At least 100 active bars in total are needed, with at least 40 in each volume half; fewer is inconclusive.
