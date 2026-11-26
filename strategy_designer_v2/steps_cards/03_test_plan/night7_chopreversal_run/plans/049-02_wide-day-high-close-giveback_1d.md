---
idea: 049-02_wide-day-high-close-giveback
brief: 049_wide-day-close-location-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e8f4c1171351
---
Fidelity:
- Situation: a coin closes high in its day's high-low range on a day whose range is wide -> adapted: graded, built as the day's range in usual ranges minus the close's distance under the high in usual ranges (each standardised).
- Comparison: the day's range against the coin's usual daily range over the past 30 days -> kept: the mean bar range of the last 30 daily bars.
- Outcome: a fall over the next day, larger the higher the close and the wider the day -> kept: short sized by the reading, horizon 1 daily bar.
- Verdict transfer: yes: the forecast grows with both the close's height in the range and the day's width, and it is judged on the next day's move against holding the coin.
Forecast: The forecast has two components on daily bars, each standardised over 60 bars with min_periods 20, at equal weight 1. The first is the day's range against its 30-day mean bar range (`RangeCompressionRatioComponent`, short_period 1, long_period 30, form "width", base "mean_bar_range"), negated. The second is the close's distance below the day's high in the same 30-day mean ranges (`BreakoutInMeanRangesComponent`, period 1, base_period 30, side "below", high_current 1). Both share the same base, so the forecast is about 5 × (width multiple) × (1 − 2 × the close's place from the low). That works because the second component's usual size is about half the first's. The forecast is negative (short) when the close sits in the upper part of the day's range and positive when it sits in the lower part. It is near 0 at mid-range or on a narrow day. Its size grows with the close's distance from the middle and with the day's width against usual. The position is never switched on or off by a threshold.
Config: 049-02_wide-day-high-close-giveback_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar (the 1-bar grid), take the slope of the coin's next-day return minus its mean daily return over all windows, regressed on the forecast. Pool all coins and windows, and cluster the standard errors by day.
- Supporting check: On bars with |forecast| in the top fifth, the mean of sign(forecast) × that excess return must be above its mean on the bottom two fifths: the lean grows with the day's width.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ −2, which means continuation in the direction of the wide day's close.
- Inconclusive: Any t between −2 and 2, or a confirming slope whose supporting check fails. At least 1,000 distinct days with a forecast are required.
