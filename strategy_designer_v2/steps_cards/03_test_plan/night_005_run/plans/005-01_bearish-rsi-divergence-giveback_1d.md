---
idea: 005-01_bearish-rsi-divergence-giveback
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new 30-day high -> kept: a 30-bar closing high from BarsSinceHighComponent(lookback 30), used as a regime rule.
- Comparison: the 14-day RSI is below its reading at the previous high in that window, and the gap is graded -> replaced: no catalogue component reads RSI at an earlier swing high.
- Outcome: the price falls over the next 10 days, more when the RSI shortfall is larger -> kept: a short position sized by the gap, judged on the 10-bar return.
- Verdict transfer: no: without RSI at the previous high, any stand-in such as the RSI level would test a different quantity, which the brief excludes.
Reason: Everything the idea needs comes from one coin's own closes, and a regime plus a graded component could hold it. But no catalogue component, alone or combined, gives the RSI value at the previous highest close in the 30-bar window. RSIPullbackComponent gives only the current RSI, and no op looks back to the bar of an earlier high.
