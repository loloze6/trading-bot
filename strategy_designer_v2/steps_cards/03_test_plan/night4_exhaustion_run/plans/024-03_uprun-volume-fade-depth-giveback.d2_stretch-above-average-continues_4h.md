---
idea: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 9111077ea370
---
Fidelity:
- Situation: price standing above its 30-day average, the further the stronger -> kept
- Comparison: the close against its average price of the past 30 days (180 bars) -> kept
- Outcome: the coin rises more over the next three days (18 bars), the further above it stands -> kept
- Verdict transfer: yes: the forecast is exactly the graded distance above the 30-day average, so its link to the next 18-bar rise tests the idea directly.
Forecast: The forecast is built from one indicator, the percent distance of the close from its 180-bar simple moving average (30 days of 4h bars). The distance is standardised against its own past 180 values, with at least 45 past values needed. The result is then clipped at 0. When the close is above the average, the forecast is long. The long position grows in proportion to how far above the average the close stands, and is capped at +20. When the close is at or below the average, the situation is absent and the forecast is 0 (flat). It never goes short.
Config: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The sample is the non-overlapping 18-bar grid of each window, all coins pooled. On it, regress each cell's forward 18-bar return, minus that coin's mean 18-bar return over all its windows, on the cell's forecast. The reading is the t of the slope.
- Supporting check: Take the grid cells with forecast > 0. Their mean excess 18-bar return, against the coin's mean drift, must be above 0.
- Confirm: The idea is confirmed when both of these hold: - the slope's t is +2 or more; - the supporting check passes, with the mean excess return of the positive-forecast cells above 0.
- Reject: The idea is rejected when the slope's t is -2 or less: larger distances above the average are followed by smaller excess rises.
- Inconclusive: A slope t between -2 and +2 is inconclusive. So is a slope t of +2 or more when the positive-forecast cells' mean excess return is not above 0. The test needs at least 200 grid cells with forecast > 0; with fewer, it is inconclusive.
