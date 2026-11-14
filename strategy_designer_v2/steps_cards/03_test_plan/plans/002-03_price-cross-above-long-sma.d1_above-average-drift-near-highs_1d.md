---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its long moving average -> kept: a regime rule on the close's distance from its 200-day SMA.
- Comparison: drift larger nearer the recent high and after a stronger recent rise, fading on pullbacks -> adapted: the on/off reading is made graded, using range position plus 20-day rise, so the long shrinks as the close falls back.
- Outcome: price keeps drifting upward -> kept: forward return of the coin, long side only.
- Verdict transfer: yes: the forecast is the idea's own graded long inside its own condition, so a gain or loss on it bears directly on the idea.
Forecast: When the close is above its 200-day SMA, the forecast is the average of two parts. The first is where the close sits in its 20-day closing range. The second is the 20-day percent rise. Each part is standardised over 60 bars and clipped at 0. The forecast grows as the close nears its 20-day high and as the rise strengthens. It shrinks toward 0 as the close pulls back into the lower half of the range or the 20-day change turns negative. It is never negative. It is 0 on every bar where the close is at or below the 200-day SMA.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take the grid bars (positions 0, 20, 40, ... of each window) where the forecast is above 0. On each, compute allocation (forecast/10) x (the coin's next 20-bar return minus the coin's mean 20-bar return over all windows). Report the t of the mean, before costs.
- Supporting check: The book's Calmar, before costs, is at least the Calmar of holding the coins over the same windows.
- Confirm: The mean is above 0 with t ≥ 2 on at least 100 cases, and the Calmar check passes.
- Reject: The mean is below 0 with t ≤ -2 on at least 100 cases.
- Inconclusive: Any t between -2 and 2, or a confirming t with the Calmar check failing, or fewer than 100 grid cases with a positive forecast.
