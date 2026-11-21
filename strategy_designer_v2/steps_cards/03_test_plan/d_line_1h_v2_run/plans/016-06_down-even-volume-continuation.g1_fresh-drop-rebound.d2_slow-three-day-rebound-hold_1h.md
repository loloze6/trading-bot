---
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has fallen over the past 3 days, and the size of its fall over the last 1 day -> adapted: the 72-bar fall is a regime condition ("while", not "after"), and the 24-bar fall is a graded size.
- Comparison: the larger the 1-day fall, the larger the rise -> kept: the position grows with the 24-bar fall, and the gain is judged against position size.
- Outcome: price rises over the next 3 days, the rise building across all 3 days, not just the first hours -> kept: 72-bar horizon and hold, with a check on bars 24 to 72.
- Verdict transfer: yes: the test measures this exact situation, size and horizon, so a confirm or reject applies to the idea itself.
Forecast: A rule selects the active regime. When the 72-bar price change is below 0 (the coin fell over 3 days), the regime is mean_reversion; otherwise it is flat. In mean_reversion the forecast is the 24-bar percent price change. It is standardised (window 60, min_periods 20), negated so that a fall reads positive, and clipped at 0 so it is long only. The forecast is 0 when the last day rose. It grows smoothly with the depth of the 1-day fall: about +10 for a usual-sized fall, capped at +20. It is never negative.
Config: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use a non-overlapping 72-bar grid in each window, keeping only grid bars with forecast > 0. On those bars, regress the coin's next-72-bar return minus its mean 72-bar return over all windows on the forecast. The measure is the slope's t-statistic, before costs.
- Supporting check: On the same grid bars, take the forecast-weighted mean of the excess return from bar t+24 to bar t+72 (the coin's mean 24-to-72-bar move subtracted). It must be above 0, meaning the rise is not spent in the first day.
- Confirm: The slope's t is 2 or more, and the supporting check is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t strictly between -2 and 2 is inconclusive. So is a t of 2 or more when the check fails. The test needs at least 100 grid cases with forecast > 0, pooled over coins and windows; below that it is inconclusive.
