---
idea: N1-05_friday-to-saturday-rise
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the bar is Friday's daily close, held into Saturday -> replaced: no catalogue component reads the weekday from the timestamp.
- Comparison: the coin's average daily return -> kept: the coin's mean daily return over all windows serves as the benchmark.
- Outcome: the Friday-to-Saturday close-to-close return is higher than average -> kept: measured as the next bar's return on the position opened at Friday's close.
- Verdict transfer: no: without a weekday reading, no forecast can single out the Friday-to-Saturday bar, so no result would bear on the idea.
Reason: The idea's situation is a calendar day. The timestamp column is in the coin's own bars, and a graded per-bar forecast could hold this idea. But no catalogue component, alone or combined, turns the timestamp into a weekday reading. The only components that read the timestamp check the UTC hour, which is always 0 on 1d bars. The regime detector cannot read the weekday either.
