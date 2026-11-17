---
idea: 013-04_heavy-volume-below-high-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: the coin closes above its prior 52-week high -> kept
- Comparison: volume over the preceding 10 days against its own 90-day average, heavier meaning larger -> kept
- Outcome: the return over the next 30 days is larger, upward, the heavier that volume -> adapted: "after the break" becomes "while above the prior high", and the 30-day hold is dropped from the position, but the criterion still measures the 30-bar return.
- Verdict transfer: yes: the criterion measures the 30-bar forward return of breakout bars against the graded volume reading, which is exactly the idea's claim.
Forecast: The forecast is zero unless today's close is above the highest high of the prior 365 daily bars, with today left out. On those breakout bars, the forecast is long. It equals the 10-bar mean volume (today included) divided by the 90-bar mean volume, standardised against its own past 90 values. It is therefore about +10 when the volume ratio is at its usual size, larger (up to +20) when volume before the break was heavier, and smaller when it was lighter. It is never negative.
Config: 013-04_heavy-volume-below-high-breakout_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The cases are breakout events: bars with regime "trending", de-duplicated per coin and window so that each event is at least 30 bars after the previous one and has a full 30 bars ahead inside its window. For each event, take the excess return: its 30-bar forward return minus the coin's mean 30-bar return over all windows. The measure is Welch's t of the mean excess return of events in the top half of forecast minus that of events in the bottom half.
- Supporting check: none
- Confirm: Welch t >= 2.0, with the top half minus the bottom half positive, with at least 30 events.
- Reject: Welch t <= -2.0, with heavier pre-break volume followed by smaller excess returns, with at least 30 events.
- Inconclusive: Any t between -2.0 and 2.0, or fewer than 30 de-duplicated breakout events across all coins and windows.
