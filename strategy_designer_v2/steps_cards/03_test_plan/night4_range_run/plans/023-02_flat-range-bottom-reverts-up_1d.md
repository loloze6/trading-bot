---
idea: 023-02_flat-range-bottom-reverts-up
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: a coin's close sits below the middle of its 30-day high-low range -> kept: the percent distance of the close below the midpoint of the 30-bar high-low range, through `IchimokuCloudPositionComponent` with all periods 30 and displacement 0.
- Comparison: the 30-day net move is small next to the 30-day high-low range -> kept: a regime rule on `NetMoveToRangeRatioComponent` (30, high_low) at or below 0.3, a conventional "no trend" cut.
- Outcome: the further below the middle, the more it rises over the next 5 days -> kept: a long position that grows with the distance below the middle, held for 5 daily bars.
- Verdict transfer: yes: the position is sized by exactly the idea's distance, only in the idea's flat situation, and judged on the idea's 5-day rise.
Forecast: The forecast is active only on days when the 30-bar net close move is at most 0.3 of the 30-bar high-low range. On other days it is 0. On active days it is built from the close's distance from the midpoint of the 30-bar high-low range, as a percent of the close. That distance is standardised over its past 60 values and negated, so a close below the middle reads positive. It is then clipped at 0. The forecast is positive and grows linearly the further the close sits below the middle (about +10 at a typical distance, capped at +20). It is 0 at or above the middle. It is never short.
Config: 023-02_flat-range-bottom-reverts-up_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, all coins pooled. Take the cases where the forecast is above 0. For each case, compute the coin's 5-bar forward return minus the coin's normal 5-bar drift over all its windows. The measure is the mean of that excess return, with its t.
- Supporting check: Among those cases, the mean excess return of the half with the larger forecast minus that of the half with the smaller forecast is above 0.
- Confirm: The mean excess 5-bar return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean excess 5-bar return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 when the larger-forecast half does not beat the smaller one. So is any result with fewer than 30 independent cases.
