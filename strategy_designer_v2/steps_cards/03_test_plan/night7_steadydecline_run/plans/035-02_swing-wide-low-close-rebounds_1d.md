---
idea: 035-02_swing-wide-low-close-rebounds
brief: 035_wide-day-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a day's high-to-low range, as a multiple of the 20-day std of daily returns, with the close near the day's low -> replaced: no component gives the range in 20-day return stds, or its product with the close's nearness to the low.
- Comparison: wider days against narrower days, both closing near their low -> kept: a graded forecast that grows with the width compares them.
- Outcome: the coin rises over the next day, more after wider days -> kept: a 1-bar horizon on 1d bars, long only.
- Verdict transfer: no: the closest components measure the range against the mean bar range, or the location times the std, which are different quantities.
Reason: The idea needs bar t's range divided by the close and by the 20-day std of one-bar returns, multiplied by where the close sits in the bar (the nearer the low, the larger). No catalogue component computes this. A weighted mean can only add standardised components, not multiply them. vol_normalize divides by the std of the close in price units over 24 bars, not by the std of returns over 20 days.
