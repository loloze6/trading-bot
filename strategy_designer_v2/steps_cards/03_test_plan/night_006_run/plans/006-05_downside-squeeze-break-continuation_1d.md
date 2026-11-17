---
idea: 006-05_downside-squeeze-break-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a close below the low of a tight 20-day band -> kept: a regime rule on DonchianBreakoutComponent(20) at its floor (-20) marks a close at the lowest of 20 closes.
- Comparison: how narrow the 20-day band is against the coin's 100-day range -> replaced: no catalogue component computes this width ratio, alone or combined.
- Outcome: price keeps falling past the band's bottom over the next 3 days, downward -> kept: a short whose size grows with narrowness, judged on 3-bar forward returns.
- Verdict transfer: no: without the 20-day-to-100-day range ratio, the size could not follow the idea's narrowness, so neither a confirm nor a reject would carry over.
Reason: The bars hold everything the idea needs, and a regime plus a graded short could carry it. No component measures the 20-day high-low width against the 100-day high-low width, and the config can only take weighted sums, not ratios. `standardise` on a 20-day width judges it against its own past, not against the 100-day range.
