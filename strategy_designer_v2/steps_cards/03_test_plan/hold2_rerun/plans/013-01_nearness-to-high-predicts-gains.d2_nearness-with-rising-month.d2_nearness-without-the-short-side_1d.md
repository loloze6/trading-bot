---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the daily close sits close to its 52-week high and far above its 52-week low, while the 30-day return is positive -> adapted: closeness is graded as the close's position in its 364-bar range, and the "only while" condition is a regime on the 30-bar return.
- Comparison: near the high versus far below it, and a higher versus a lower 30-day return -> kept: both are graded, so the size grows with each.
- Outcome: a higher return over the next 7 days, upward, with no short positions -> kept: 7 bars, long only.
- Verdict transfer: yes: the forecast is long in proportion to range position and 30-day return only while that return is positive, which is exactly what the idea claims.
Forecast: The regime is active on bars where the 30-bar return (PriceEvolutionComponent, period 30) is above 0. On all other bars the forecast is flat. Inside that regime, the forecast is the equal-weight mean of two parts. The first is the close's position in its 364-bar closing range (DonchianBreakoutComponent, period 364), standardised over 364 bars and clipped at 0. It grows as the close nears the 52-week high and moves away from the 52-week low, and it is 0 in the lower half of the range. The second is the 30-bar return, standardised over 60 bars and clipped at 0. It starts at 0 when the return turns positive and grows with the return. The forecast is never negative. It is largest when the coin is near its high after a strong 30-day rise. A coin far below its high but rising gets only a small long position.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Take the grid bars (positions 0, 7, 14, ... of each window) where forecast > 0. For each one, compute the 7-bar forward return minus that coin's mean 7-bar return over all windows on the same grid. Report the t of the mean of these excess returns, pooled across coins.
- Supporting check: Split the forecast > 0 grid bars at the forecast's median. The mean excess return of the upper half minus that of the lower half must be above 0.
- Confirm: The main measure's t is 2 or more and the supporting check passes.
- Reject: The main measure's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with the check failing, is inconclusive. Fewer than 100 independent forecast > 0 cases is also inconclusive.
