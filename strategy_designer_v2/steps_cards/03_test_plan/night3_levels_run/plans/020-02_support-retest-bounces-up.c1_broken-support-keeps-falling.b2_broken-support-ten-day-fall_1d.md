---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close just below prices where the coin turned up several times in the past 90 days -> kept: `SwingHighClusterCountComponent` with `pivot` "low", `level` "above" and `period` 90 finds the lowest past swing low at or above the close and weights by nearness to it.
- Comparison: the more such turning-up lows just above the close, the larger the fall -> kept: the "proximity" form multiplies the count of swing lows within the band of that level by the close's nearness, so the position grows with the count.
- Outcome: price falls over the next 10 days -> kept: the forecast is short (negated) and the book holds each bet for 10 daily bars.
- Verdict transfer: yes: the forecast is short in proportion to the count of nearby past turning-up lows above the close, held 10 days, so its 10-day results confirm or reject the idea.
Forecast: One component, `SwingHighClusterCountComponent` (period 90, side 2, band 2 %, pivot "low", level "above", form "proximity", power 1). It takes L, the lowest confirmed 90-day swing low at or above today's close. It counts N, the swing lows within 2 % of L. Its value is N x 1/(1 + D), where D is the close's percent distance below L. That value is standardised against its own last 90 values (target 10, cap 20) and negated, so the forecast is never positive. It is zero when no past turning-up low sits at or above the close. It grows more negative (a larger short) the more lows cluster at the level and the nearer the close sits just under it, up to -20.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The grid is every 10th bar of each window, with returns kept inside each window. On each grid bar where the forecast is below 0, take -(forecast/10) x (the coin's 10-bar return minus its normal 10-bar drift over all windows). The measure is the mean of these values and its t-statistic: the short's gain beyond holding the coin, sized by the position.
- Supporting check: Split those grid bars at the median of |forecast|. The mean drift-adjusted 10-bar fall (in the short direction) must be larger for the larger-forecast half than for the smaller half (Welch difference > 0).
- Confirm: The main mean is > 0 with t >= 2, and the supporting difference is > 0.
- Reject: The main mean is < 0 with t <= -2, meaning the coin rises beyond its drift after these closes.
- Inconclusive: Any t between -2 and 2, or a confirming main measure whose supporting difference is <= 0. Also inconclusive if there are fewer than 100 non-overlapping grid cases with forecast below 0 across all coins and windows.
