---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: how much the coin has risen over its last 7 days -> kept: 168-bar percent return, graded, long side only.
- Comparison: none. The idea's "the more ... the more" is the graded size of the rise -> kept.
- Outcome: the coin rises more over the next 3 days -> kept: held for 72 bars and judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the 7-day rise itself and is judged on the next 3 days' excess return, so a confirm or a reject applies to the idea as stated.
Forecast: The forecast is the coin's percent change over the last 168 hourly bars (7 days). It is standardised against the mean absolute size of its own previous 168 values, so an average-sized week reads about 10, capped at 20. Below zero it is clipped to 0, so it is long only. It is 0 after a 7-day fall. It is positive after a 7-day rise and grows in proportion to the size of the rise. The idea speaks only of rises and its consequence is to stay long, so a fall is not turned into a short.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the non-overlapping 72-bar grid of each window (positions 0, 72, 144, ...). For each grid bar, compute the 72-bar forward return minus the coin's normal 72-bar drift (its mean over all windows). Multiply that by the bar's forecast / 10. Take the ordinary t of the mean of this product, pooled over all coins and windows. This is the gain that grows with the position, net of holding the coin.
- Supporting check: On the same grid, the mean excess 72-bar return of cells with a forecast above the median of the positive forecasts must exceed that of cells with forecast 0.
- Confirm: The main measure has t ≥ 2 and the supporting check passes (top-half excess return minus zero-forecast excess return > 0).
- Reject: The main measure has t ≤ -2. Larger 7-day rises are followed by 3-day returns below the coin's drift.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a failed supporting check, is neither confirm nor reject. The test needs at least 200 grid cases with a positive forecast and at least 200 with a zero forecast; with fewer, it is inconclusive.
