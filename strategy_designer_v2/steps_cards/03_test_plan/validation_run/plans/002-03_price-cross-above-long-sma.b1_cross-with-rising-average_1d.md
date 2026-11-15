---
idea: 002-03_price-cross-above-long-sma.b1_cross-with-rising-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close has crossed above its long moving average -> adapted: "after the cross" becomes "while the close is above its 200-day SMA".
- Comparison: only while the long average is rising, and the faster it rises the larger the move; judged against holding the coin -> adapted: the "rising" on/off condition is a regime gate, and the rise speed is graded by the 200-day SMA's 20-bar slope.
- Outcome: price keeps rising further than holding the coin -> kept.
- Verdict transfer: yes: the test measures excess forward return while the close is above a rising long average, and how that return grows with the slope, which is exactly the idea's claim.
Forecast: The regime detector checks two things on every bar: the close's percent distance from its 200-day SMA, and the 20-bar percent slope of that SMA. The regime is "trending" only when both are above 0 (close above the average, average rising). On every other bar the regime is "unknown", which is set flat (forecast 0). Inside "trending", the forecast is the SMA200 slope, standardised against its own past 220 values (target 10, cap 20) and clipped at 0. It is long only and positive, and it grows with how fast the long average rises: about 10 at an average slope, up to 20 at twice the average or more. When the close falls below the average, or the average stops rising, the forecast is 0.
Config: 002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take non-overlapping 20-bar samples on each window's grid. For the cases with forecast > 0 at bar t, take the coin's 20-bar forward return minus that coin's mean 20-bar return over all windows (holding). Report the mean of this excess and its t.
- Supporting check: Among the active cases, regress the excess 20-bar return on the forecast at bar t. The slope coefficient must be above 0 (faster-rising average, larger move).
- Confirm: The idea is confirmed only if both hold: - the main measure's mean excess is above 0 with t ≥ 2; - the supporting check's slope coefficient is above 0.
- Reject: The mean excess return of the active cases is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t ≥ 2 with a slope coefficient ≤ 0 is also inconclusive. Fewer than 30 active non-overlapping cases across all coins and windows is inconclusive.
