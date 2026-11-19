---
idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: coin has risen over the past 2 to 3 days, with a share of its hourly movement going in the rise's direction (net move over the sum of absolute hourly moves) -> kept: a regime requires a rise over both 48 and 72 bars, and an unsmoothed 72-bar efficiency ratio measures the share.
- Comparison: higher versus lower share among rises ("the more ... the more"), a choppy rise of the same size staying out -> kept: the position grows with the efficiency ratio and is near zero for a choppy rise.
- Outcome: the coin rises more over the next 3 days -> adapted: "after X" becomes "while X", and the 3-day holding period is dropped; it is judged on 72-bar forward returns.
- Verdict transfer: yes: the forecast scales a long position by the same ratio, only while the rise holds, so gains that grow with it confirm the idea and losses that grow with it reject it.
Forecast: The forecast is computed only on bars where the close is above its level 48 bars ago and also above its level 72 bars ago (the "trending" regime); on all other bars it is 0 (flat). In the trending regime it is the 72-bar Kaufman efficiency ratio, unsmoothed (smooth_period 1). This is abs(net 72-bar change) over the sum of the absolute one-bar changes. Inside the regime the net change is positive, so this equals net rise over total movement. The ratio is standardised against its own past 72 values (target 10, cap 20), so the forecast is always long. It is near 0 when the rise is tiny relative to the hourly chop. It is about +10 at the ratio's usual size and up to +20 for a very smooth rise. Because the ratio tends to 0 as the net rise tends to 0, the position grows from near zero at the regime's edge rather than jumping.
Config: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use a non-overlapping 72-bar grid in each window, keeping only grid bars with forecast > 0. On each, take the coin's forward 72-bar return minus the coin's mean 72-bar return over all its windows. Regress this excess return on the forecast, pooled over coins and windows, and report the t of the slope.
- Supporting check: On those grid bars, the forecast-weighted mean excess 72-bar return (sum of forecast x excess over sum of forecast) is above 0.
- Confirm: The slope's t is ≥ 2 with at least 200 cases, and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is ≤ -2 with at least 200 cases.
- Inconclusive: Any of the following is inconclusive: - a slope t between -2 and 2; - a t of 2 or more while the weighted mean excess return is ≤ 0; - fewer than 200 non-overlapping grid bars with forecast > 0.
