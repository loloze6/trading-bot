---
idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has risen over the past 3 days -> kept: the residual share is 0 unless the 72-bar net return is above 0.
- Comparison: the share of that rise from its few biggest hourly gains, smaller meaning more of a grind -> kept: 1 minus the share of the rise from the 3 largest hourly gains, over 72 bars.
- Outcome: the coin keeps rising over the next 3 days, more so the smaller that share -> adapted: "after the rise" made "while the rise holds", with the 3-day hold dropped; the outcome is still read on the 72-bar forward return.
- Verdict transfer: yes: the forecast grows with the evenness of the rise, and the test reads the next 72 bars.
Forecast: One component, `TopGainsShareOfRiseComponent` with period 72, k 3 and form "residual". It is 0 when the coin has not risen over the last 72 hourly bars. Otherwise it is 1 minus the share of the rise carried by the 3 largest hourly gains, so it grows toward 1 as the rise spreads over many small hours. It is standardised against its own last 72 values, so an average grind gives about +10, capped at +20. The forecast is never negative: long, and larger the more evenly the 3-day rise was built; zero when there was no rise. Moving from a slight rise to no rise brings it smoothly to 0.
Config: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the non-overlapping 72-bar grid of each window, pooled over coins and windows, using bars with forecast > 0. For each bar, take the forward 72-bar return minus the coin's mean 72-bar return over all windows. Regress this excess return on the forecast and read the t of the slope.
- Supporting check: On the same bars, the forecast-weighted mean of that excess forward return must be above 0.
- Confirm: The idea is confirmed when the slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reject: The idea is rejected when the slope's t is -2 or less: the more evenly built the rise, the less the coin rises next.
- Inconclusive: Results in between are inconclusive. These are a slope t between -2 and 2, or a t of 2 or more with a weighted mean excess return of 0 or below. At least 100 independent grid cases with forecast > 0 are required; fewer is inconclusive.
