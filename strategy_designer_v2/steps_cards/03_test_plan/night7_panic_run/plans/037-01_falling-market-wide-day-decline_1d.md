---
idea: 037-01_falling-market-wide-day-decline
brief: 037_wide-days-precede-decline-in-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a falling market, a day whose high-low range is wide against the coin's 30-day standard deviation of daily returns -> replaced: no component divides a bar's range by the standard deviation of returns; the nearest one, the range over the mean bar range (`RangeCompressionRatioComponent` "width"), is a different quantity.
- Comparison: the wider the range in units of that swing, the larger the decline -> adapted: the forecast grows with the range multiple, inside the "wide" regime.
- Outcome: price declines over the next 3 days -> kept: a short position held 3 bars.
- Verdict transfer: no: a test on range over mean bar range, or over a 24-bar price-level std, would not measure the idea's range in units of the 30-day return std.
Reason: The idea's situation is the day's high-low range in units of the coin's 30-day standard deviation of daily returns. No catalogue component computes it. Weighted means cannot divide one component by another. `vol_normalize` uses `stddev_24`, which is a 24-bar standard deviation of price levels, not of returns. No component outputs the raw range in price units for it to act on anyway.
