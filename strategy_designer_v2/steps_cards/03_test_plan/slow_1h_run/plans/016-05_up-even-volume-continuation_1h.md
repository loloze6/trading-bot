---
idea: 016-05_up-even-volume-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: coin has risen over the past 3 days, with hourly volume spread evenly over those hours -> kept: the rise is a regime (72-bar close change above 0) and evenness is the median/mean of the 72 hourly volumes.
- Comparison: more even volume against less even volume during such rises -> kept: the long position grows with the evenness reading.
- Outcome: the coin keeps rising over the next 3 days, more so the more even the volume -> kept: the 72-bar forward return, compared across evenness levels.
- Verdict transfer: yes: the test measures whether rises with more even volume rise more over the next 72 bars, as the idea states.
Forecast: A regime marks bars where the close is above its level 72 bars ago (`trending`). All other bars are flat. On trending bars the forecast is the 72-bar volume evenness, the median divided by the mean of the last 72 hourly volumes, standardised over its own past 72 values. It is always positive, so the position is long. It sits near +10 at the usual evenness, rises toward the cap of 20 when volume is more even than usual, and falls toward 0 when a few hours carry the volume. It is zero whenever the coin is not up over the past 72 bars.
Config: 016-05_up-even-volume-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use trending bars with a forecast above 0, on the non-overlapping 72-bar grid of each window, pooled over coins and windows. For each bar, take the 72-bar forward return minus that coin's mean 72-bar return over all windows. Then take the top third minus the bottom third of these bars ranked by forecast, as a Welch t.
- Supporting check: The top-third bars' mean excess 72-bar return (over the coin's mean) is above 0.
- Confirm: Welch t of the top-minus-bottom difference is 2 or more, and the top third's mean excess return is above 0.
- Reject: Welch t of the top-minus-bottom difference is -2 or less.
- Inconclusive: A t between -2 and 2 is inconclusive. So is t of 2 or more with a top-third excess at or below 0. The test needs at least 30 independent grid cases in each of the top and bottom thirds; with fewer, it is inconclusive.
