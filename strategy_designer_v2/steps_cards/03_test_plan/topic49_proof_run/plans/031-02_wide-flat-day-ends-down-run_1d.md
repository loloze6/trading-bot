---
idea: 031-02_wide-flat-day-ends-down-run
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: after a 5-day fall, a day closing near its open with an unusually wide range against its 30-day average -> adapted: a regime that holds only on such days, with the forecast graded by the range multiple inside it; "wide" is a range of at least 1.5x the 30-day mean bar range and "near its open" is a body of at most 10% of the range (the doji convention), since the idea gives neither number.
- Comparison: the day's range against its 30-day average range -> kept
- Outcome: a rise over the next 5 days, larger the wider the range -> kept
- Verdict transfer: yes: the test holds long only on the idea's days, sized by the range multiple, for 5 days, so its result is the idea's.
Forecast: The forecast is zero on every bar except one that meets all three conditions: - the close is below the close 5 bars earlier (PriceEvolution, 5 bars, below 0); - the bar's range is at least 1.5 times the 30-bar mean bar range (RangeCompressionRatio, short window 1, long window 30, base "mean_bar_range", form "width"); - the body is at most 10% of the range (BarBodySize, measured against the range, form "flatness", at least 0.9). On such a bar the forecast is long. It equals the range multiple standardised against its own past 60 values: about +15 at 1.5x the usual range, rising with the width, and capped at +20 from about 2x. It is never negative.
Config: 031-02_wide-flat-day-ends-down-run_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Per case (a long bet on a mean_reversion bar, read once per 5-bar grid cell), the coin's 5-bar return from that bar's close minus the coin's normal 5-bar drift over all windows. Its mean is tested with a t-statistic, counting cases on the same day as one.
- Supporting check: Over the cases, the slope of the unusual move on the forecast at the signal bar is above 0 (wider days, larger rise).
- Confirm: The mean unusual move is positive with t >= 2, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a slope of 0 or below. Fewer than 30 cases (case days) is inconclusive whatever the t.
