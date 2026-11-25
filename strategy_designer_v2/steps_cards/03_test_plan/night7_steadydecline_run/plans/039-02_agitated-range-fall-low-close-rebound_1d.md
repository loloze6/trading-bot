---
idea: 039-02_agitated-range-fall-low-close-rebound
brief: 039_agitated-low-close-big-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: in an agitated market, a one-day fall whose close sits near the day's low -> adapted: the agitated profile is the regime, and the fall times the close's nearness to the low is graded.
- Comparison: the fall measured against the coin's 30-day average daily range -> replaced: the only catalogue form, `FallCloseLocationComponent`, divides the fall by the standard deviation of daily returns, not by the average high-low range.
- Outcome: a larger rise over the next day, growing with both together -> kept.
- Verdict transfer: no: the idea differs from its siblings precisely by reading the usual swing as the average daily range, so a test on the return standard deviation would judge a different idea.
Reason: No catalogue component, and no weighted-mean composition, divides a one-day fall by the 30-day mean high-low range and multiplies it by the close's nearness to the day's low. `FallCloseLocationComponent` uses the return standard deviation instead. `RiseTimesRangeMultipleComponent` multiplies the fall by the bar's range multiple. `BreakoutInMeanRangesComponent` measures the distance below a high, not the fall from the prior close. A weighted mean cannot form the product.
