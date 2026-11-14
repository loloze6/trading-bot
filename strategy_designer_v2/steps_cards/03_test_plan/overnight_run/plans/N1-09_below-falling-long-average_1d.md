---
idea: N1-09_below-falling-long-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close below its 200-day average, and that average falling steeply over the past few weeks -> replaced: no component measures the 200-day average's change over weeks; the nearest one, the 200-bar price change, is that average's one-bar slope.
- Comparison: the coin's usual drift over 10 days -> kept: judged against the coin's mean return over all windows.
- Outcome: the coin keeps falling over the next 10 days -> kept: a graded short position whose 10-bar returns are measured.
- Verdict transfer: no: a test built on the one-bar slope of the average would not test whether the average has been falling steeply for weeks.
Reason: The idea needs the change in the 200-bar simple average over several weeks, for example SMA200 today against SMA200 20 bars ago. That is the mean of the last 20 closes against the mean of the closes 200 to 219 bars ago, and no catalogue component or composition compares those. The history ops that could smooth a one-bar slope (`ema`) cannot sit beside `standardise`, so the 200-bar price change cannot be averaged into a weeks-long slope either.
