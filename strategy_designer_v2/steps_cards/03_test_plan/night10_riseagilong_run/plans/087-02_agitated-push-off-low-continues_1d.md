---
idea: 087-02_agitated-push-off-low-continues
brief: 087_rising-agitated-short-push-continues
data-instruments: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a rising agitated market, the close stands far above its lowest close of the last 3 days, in units of the 30-day daily swing -> replaced: the catalogue measures distance from a 3-day low only in percent (`DistanceFromHighComponent`, `extreme` "low") or in mean bar ranges (`BreakoutInMeanRangesComponent`), never in the 30-day standard deviation of daily returns. The profile itself is added by code.
- Comparison: the farther above the low, the larger the further rise -> adapted: graded, so the position grows with the swing-scaled distance.
- Outcome: the coin keeps rising over the next 3 days (long) -> kept: held for 3 bars.
- Verdict transfer: no: built from a substitute unit (percent or bar range instead of the 30-day return swing), the test would judge a different measure of "far above the low".
Reason: The idea needs the close's distance above its 3-day lowest close divided by the standard deviation of the last 30 daily returns. No component computes this, and no composition can build it. `VolatilityScaledDistanceFromHighComponent` measures only from the high. `DistanceFromHighComponent` with `extreme` "low" gives only percent or proximity. `BreakoutInMeanRangesComponent` scales by mean bar range. `vol_normalize` divides by a 24-bar price standard deviation times the close, which is not the 30-day return swing. The config cannot divide one component by another.
