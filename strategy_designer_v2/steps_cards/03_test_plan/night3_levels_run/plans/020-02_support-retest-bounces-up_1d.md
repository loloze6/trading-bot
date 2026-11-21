---
idea: 020-02_support-retest-bounces-up
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: price falls back to a price where it turned up several times in the past 90 days -> adapted: "falls back" becomes "while the close is below its close 5 bars ago", and "several times" becomes a graded, nearness-weighted count of 90-day swing lows within 1.5% of the close.
- Comparison: the more past turns up at the level, the larger the rise -> kept: the forecast grows with the count of swing lows near the close.
- Outcome: price rises over the next 5 days -> kept: each bet is held 5 daily bars and judged against holding the coin.
- Verdict transfer: yes: the forecast is long exactly when the close falls back near repeated swing lows, sized by their count, so its 5-day outcome confirms or rejects the idea.
Forecast: The forecast comes from SwingLowTouchNearnessComponent with period 90, side 2, band 1.5 and fall_period 5. While the close is below its close 5 bars ago, the component adds, for each swing low of the last 90 bars, a nearness weight: 1 when the close sits on that low, falling to 0 at 1.5% away. When the close has not fallen, or no swing low is near, the value is 0. It is standardised against its own past 90 values (min_periods 22). It then passes through signed_power with exponent 2, a graded dead zone that damps a single nearby turn and amplifies levels touched several times. The forecast is never negative (long only by construction). It is zero away from such levels, and grows with the number of past turns at the level and with how close the price is to it.
Config: 020-02_support-retest-bounces-up_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward return from the close of each case (a forecast rise of at least 2 points, one per 5-bar grid cell per window) minus the coin's normal 5-bar drift over all windows. Take the mean of these excess returns, weighted by the case's forecast, with its t across the cases pooled over coins.
- Supporting check: Across the cases, the Spearman correlation between the forecast and the 5-bar excess return is positive (larger counts give larger rises).
- Confirm: The forecast-weighted mean excess return is positive with t >= 2, and the supporting correlation is above 0.
- Reject: The forecast-weighted mean excess return has t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t >= 2 with a correlation of 0 or below is also inconclusive. Fewer than 30 independent cases in total is too few to judge.
