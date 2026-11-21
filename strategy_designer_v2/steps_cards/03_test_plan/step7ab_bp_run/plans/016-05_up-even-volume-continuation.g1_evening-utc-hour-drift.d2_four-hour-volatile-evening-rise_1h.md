---
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: each day, the four hours after 21:00 UTC -> kept: a regime selects the bar closing at 21:00 UTC (coming bar 21:00), and the bet is held 4 bars.
- Comparison: a larger rise than over the coin's other four-hour stretches -> kept: case returns are measured against the coin's mean 4-hour return over all windows.
- Outcome: the coin rises over those 4 hours, more so the higher its 7-day realised hourly volatility -> adapted: position size is graded by the 168-bar hourly return volatility, standardised against its own past.
- Verdict transfer: yes: the forecast bets long only on the 21:00 four-hour stretch, sized by 7-day volatility, which is exactly the idea's claim.
Forecast: Only on the bar whose close is 21:00 UTC (the coming bar is stamped 21:00), the forecast equals the standard deviation of the last 167 hourly returns (7 days), standardised against its own past 168 values. It is about +10 at the coin's usual recent volatility, higher (up to 20) when volatility is above it, and lower when it is below. It is never negative. On every other bar the regime is null and the forecast is 0. The holding period keeps each evening bet for 4 bars.
Config: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: For each case (each day's bet opened at the 21:00 UTC close), take the coin's 4-bar return from that close minus the coin's normal 4-bar drift. The normal drift is the mean return on the non-overlapping 4-bar grid of all its windows. The measure is the ordinary t of the mean of these unusual moves, pooled over coins and windows.
- Supporting check: Split each coin's cases into thirds by forecast size (7-day volatility). The mean unusual move of the top third minus that of the bottom third must be above 0.
- Confirm: The main t is 2 or more with a positive mean, and the top-minus-bottom volatility-third difference is above 0.
- Reject: The main t is -2 or less, or the top-minus-bottom volatility-third difference has a Welch t of -2 or less.
- Inconclusive: A main t between -2 and 2, or a main t of 2 or more with a volatility difference at or below 0 but Welch t above -2. At least 200 cases are needed in total, and at least 30 per volatility third; fewer cases is inconclusive.
