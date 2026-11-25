---
idea: 054-01_deep-reclaimed-low-pierce-rebound
brief: 054_reclaimed-monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: d0efaf60e7be
---
Fidelity:
- Situation: in a falling agitated market, the day's low goes below the prior 30-day low but the close is back above it -> replaced: the catalogue's lows below a prior low are all measured on the close, never on the day's low, so the pierce cannot be told apart.
- Comparison: the deeper the day's low went below the 30-day low, the larger the rise -> replaced: no component gives the low's depth under the prior low; the only nearby combination (two standardised close-to-low distances subtracted) is non-zero on ordinary days.
- Outcome: rises over the next 5 days -> kept: a long held 5 daily bars.
- Verdict transfer: no: without the low's pierce depth, the test would measure a close-based quantity, not a failed pierce of the monthly low.
Reason: The reclaim (close at or above the prior 30-day low) can be a regime rule on `DistanceFromHighComponent` (`extreme` "low", `source` "high", `exclude_current` 1, `period` 30, percent ≥ 0). No component compares the day's own low with that prior low, so neither the pierce condition nor its depth can be built. The data is in the coin's own bars (`low`), so a component is missing rather than the idea being untestable.
