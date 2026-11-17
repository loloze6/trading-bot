---
idea: 010-04_rsi-below-streak-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: 14-day RSI below 50 without a break, counted in days up to the current close -> replaced: no catalogue component counts how many bars in a row RSI has stayed below 50.
- Comparison: longer unbroken stretches against shorter ones -> kept: a graded count would size the position by the length of the stretch.
- Outcome: lower coin return over the next 14 days -> adapted: holding period dropped, a short position held while the stretch lasts, judged at 14 bars.
- Verdict transfer: no: measuring the RSI level or a price-based age in place of the RSI stretch length tests a different quantity, so neither result would transfer to the idea.
Reason: The idea needs the length of the current unbroken run of 14-day RSI below 50, which comes from the coin's own closes. No catalogue component computes it. RSIPullbackComponent gives only the RSI level. MovingAverageAgeComponent counts days on one side of a price SMA, not of the RSI midline. A veto with `consecutive_bars` tests only one fixed length, so it is on/off rather than graded.
