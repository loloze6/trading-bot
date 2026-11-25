---
idea: 045-02_agitated-wide-high-close-giveback
brief: 045_agitated-wide-day-close-location-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 0e977cd77240
---
Fidelity:
- Situation: in an agitated market, how high the coin closes in its day's range, times how wide that range is against its usual daily range over the past 30 days -> adapted: "agitated" is the brief's profile, added by code; inside it, (2 x close location − 1) x range multiple is built as two graded parts, the range multiple and the distance from the high in mean ranges.
- Comparison: the day's range against its usual daily range over the past 30 days -> kept: the 30-bar mean bar range, today included, is the divisor of both parts.
- Outcome: the higher and wider the close, the larger the fall the next day (and a close near the low, the stronger the next day) -> kept: the position is opposite to the close location, held for 1 daily bar.
- Verdict transfer: yes: the forecast is the idea's signed close-location reading scaled by range width, inside agitated bars only, judged on the next day's return.
Forecast: The forecast is built from two components, each standardised over 60/20. - `dist`: BreakoutInMeanRanges with period 1, base 30, "below", high_current 1. It is (high − close) / the 30-day mean bar range. - `width`: RangeCompressionRatio with short 1, long 30, mean_bar_range, "width". It is the day's range / the 30-day mean bar range. The forecast is dist (weight +1) minus width (weight −1). That is about −(2 x loc − 1) x the range multiple. - It is negative (short) when the close sits near the high, larger the wider the day. - It is positive (long) when the close sits near the low, larger the wider the day. - It is near zero at mid-range or on narrow days. The size is graded with both the location and the width. Code adds the agitated profile, so the book is flat on calm bars.
Config: 045-02_agitated-wide-high-close-giveback_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The timing gain, measured on bars in the profile where the forecast is not zero. On each such bar it is forecast/10 x (the coin's next-day return − that coin's mean daily return over all its windows). Cases on the same day are summed into one case per day, and the measure is the t of the mean over those days.
- Supporting check: The same timing gain per unit of |forecast| is compared between bars in the top third of |forecast| and bars in the bottom third. The top third must be higher (difference top minus bottom > 0), which shows the reversal grows with range width.
- Confirm: The main t is ≥ 2 and the supporting difference is > 0.
- Reject: The main t is ≤ −2.
- Inconclusive: Any main t between −2 and 2 is inconclusive. A main t ≥ 2 with the supporting difference ≤ 0 is also inconclusive. The test needs at least 300 days with a nonzero forecast in the agitated profile; with fewer, it is inconclusive.
