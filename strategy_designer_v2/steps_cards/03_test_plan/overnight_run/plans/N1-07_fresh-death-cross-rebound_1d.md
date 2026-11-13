---
idea: N1-07_fresh-death-cross-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the 50-day SMA crossed below the 200-day SMA within the last 20 bars -> replaced: no component holds the cross's recency, so only "SMA50 below SMA200 now" could be measured.
- Comparison: the coin's rise beats its average 10-day move -> kept: forward returns are judged against the coin's mean 10-day return.
- Outcome: the coin rises over the next 10 days -> kept: a long position paid by the next 10 daily returns.
- Verdict transfer: no: "SMA50 below SMA200" covers whole bear phases, not fresh death crosses, so neither a confirm nor a reject would carry over.
Reason: The idea needs to know, on each bar, whether the 50/200 SMA death cross happened in the last 20 bars. Every catalogue component, and every regime rule, sees only current values, never a lagged spread or the time since an event. A death-cross recency measure can be computed from the coin's own closes and fits a regime rule or a graded component, but no catalogue component computes it, alone or combined.
