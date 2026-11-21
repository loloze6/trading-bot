---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, while the close is above its 50-day average -> adapted: a regime gate on "the close crossed a 90-day swing-high close level on this bar AND the close is above its SMA50", with "several" made graded by the touch count.
- Comparison: more touches, a further close above the level and a further close above the SMA50 give a larger rise -> kept: the forecast grows with touches x margin above the level, plus the percent distance above the SMA50.
- Outcome: the coin keeps rising over the next 20 days -> kept: each bet is held 20 bars, and its 20-bar return is judged against holding the coin.
- Verdict transfer: yes: the forecast is long exactly on these breaks, sized by the idea's three strengths, and held for its 20-day horizon.
Forecast: The regime detector computes two values on each daily bar: - rb, `ResistanceBreakTouchCountComponent` (period 90, side 2, band 2, cross_period 1): it is above 0 only on a bar whose close crossed above a 90-day swing-high close level. Its value is the level's touch count x the percent margin of the close above the level. - ma, `MovingAverageDistanceComponent` (SMA, period 50): the percent distance of the close from its 50-day average. The bar is "trending" when rb > 0 and ma > 0. Every other bar is flat. In "trending" the forecast is the equal-weight mean of rb standardised (window 90, min_periods 22) and ma standardised (window 60, min_periods 20). Both are positive there, so the forecast is long only. It grows with more touches, a wider margin above the level and a larger distance above the SMA50, and it is about 0 for a break that barely clears the level near the SMA50. It is zero on every other bar, and each bet is then held for the 20-bar horizon.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Each case is a bet: a rise of the forecast of at least 2 points, taken once per 20-bar grid cell. For each case, take the coin's 20-bar return from the signal bar's close minus the coin's normal 20-bar drift (holding the coin, over all windows). The measure is the mean of this unusual move over all cases, with its one-group t, before costs.
- Supporting check: Split the cases at the median entry forecast. The upper half's mean unusual move must exceed the lower half's (upper minus lower > 0).
- Confirm: The mean unusual move is > 0 with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is < 0 with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is also inconclusive. So is any result with fewer than 30 cases.
