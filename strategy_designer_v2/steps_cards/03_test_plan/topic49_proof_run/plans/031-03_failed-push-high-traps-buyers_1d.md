---
idea: 031-03_failed-push-high-traps-buyers
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 051b3422f169
---
Fidelity:
- Situation: after a 5-day rise, a day whose high pushes above the prior 5-day high and whose close falls back near its open, graded by how far the high reached above that prior high in 30-day average ranges -> replaced: no component measures how far the day's high goes above the prior 5-day high; the catalogue's breakout components all use the close.
- Comparison: the push measured against the coin's 30-day average bar range -> kept: the 30-day mean bar range is available as the divisor inside the breakout components.
- Outcome: a fall over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: no: a close-based break measures a different day than the one the idea describes, a flat close after an intraday push, so neither result would carry over to the idea.
Reason: Every input the idea needs is in the coin's own daily bars. The run's rise, the close near the open, and the 30-day mean bar range all have components. No component computes the day's high minus the prior 5-day high. Combining two standardised breakout components to get it fails, because `standardise` scales each one by its own past mean, so their difference is not the push. No regime rule can compare two components either.
