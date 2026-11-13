---
idea: N5-02_high-below-60-day-fails
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a close at a new 20-day high -> adapted: graded as where the close sits in its 20-day range, largest at the top.
- Comparison: while the close is still below its level of 60 days earlier -> kept: a regime rule that the 60-bar price change is below 0.
- Outcome: price falls back within the next week -> adapted: a short held while the situation lasts, the one-week hold dropped.
- Verdict transfer: yes: the forecast is short only when the close is near its 20-day top inside a 60-day decline, so its 7-bar results answer the idea directly.
Forecast: The regime detector computes the 60-bar price change (PriceEvolutionComponent, period 60). A bar is `mean_reversion` when the close is below its close of 60 bars earlier, and flat (`unknown`, null) otherwise. In `mean_reversion`, the forecast uses DonchianBreakoutComponent (period 20), which says where the close sits in its 20-bar closing range: - It is standardised (60/20), so its typical size is about 10. - It is clipped at 0, so only the upper half of the range counts. - signed_power (exponent 3, pivot 10) damps it, so the position stays near 0 away from the top of the range. - It is negated, so the forecast is a short. The forecast is zero when the close is in the lower half of its range or above its 60-day-ago level. It is slightly negative in the mid-upper range. It reaches its largest short, clipped at -20, when the close makes a new 20-day high inside the decline. It is never positive.
Config: N5-02_high-below-60-day-fails_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The coin's 7-bar forward return after bars where the forecast is -10 or lower. This is compared with the coin's mean 7-bar return over all test windows together. Cases are pooled across coins, keeping at most one case per non-overlapping 7-bar block.
- Supporting check: The share of those cases whose 7-bar excess return over holding is negative.
- Confirm: The mean excess return is below 0 with t ≤ -2 on non-overlapping cases, and the supporting share is above 50%.
- Reject: The mean excess return is above 0 with t ≥ +2 on non-overlapping cases, meaning such highs keep rising.
- Inconclusive: Any t between -2 and +2, including a result near zero, is inconclusive. Fewer than 30 non-overlapping cases pooled over all coins and windows is also inconclusive.
