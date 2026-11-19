---
idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a coin that has risen over the past 3 days, with a larger share of its summed absolute hourly moves pointing up -> kept: the rise over 72 bars is the regime, and the share is (1 + ER)/2 for the 72-bar efficiency ratio, which rises with ER.
- Comparison: larger versus smaller up-share among climbs -> kept: the position grows with ER, so a choppy climb gets close to no position.
- Outcome: keeps rising more over the next 3 days -> kept: the 72-bar forward return, judged against holding the coin.
- Verdict transfer: yes: the forecast measures exactly the idea's share inside the idea's condition, over the idea's own horizon.
Forecast: The regime is set by the 72-bar price change. When it is above 0 (the coin has risen over 3 days), the bar is "trending". Every other bar is "unknown" and flat. On trending bars the forecast is the 72-bar Kaufman efficiency ratio, computed raw (smoothing span 1). This ratio is |net 72-bar move| / sum of the 72 absolute hourly moves. On a rise it equals 2 x up-share - 1. It is standardised against its own past 72 values, so about +10 at its usual level, up to +20. The forecast is always ≥ 0 and grows with how much of the hourly movement went up. It is near 0 for a choppy climb, and also near 0 at the regime boundary, where the net move is near 0. So the position never jumps.
Config: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the bars on a non-overlapping 72-bar grid in each window where regime = trending. Regress the forward 72-bar return minus the coin's mean 72-bar return over all windows on the forecast (er72 post_pipeline_value). Pool all coins and windows and report the slope's t.
- Supporting check: Among the same grid bars, the mean forward 72-bar excess return of the top third of forecasts minus that of the bottom third is above 0.
- Confirm: The slope's t is ≥ 2 and the top-minus-bottom-third difference is above 0.
- Reject: The slope's t is ≤ -2, meaning smoother climbs continue less than choppy ones.
- Inconclusive: A t between -2 and 2, or t ≥ 2 with a top-minus-bottom difference ≤ 0. Any result from fewer than 100 independent trending grid cases is also inconclusive.
