---
idea: 016-01_up-grind-price-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has risen over the past 3 days, and many small hourly gains made a larger share of that rise than its few biggest hours -> replaced: no catalogue component measures how much of a rise its biggest hours made; R-squared or efficiency ratio would measure path straightness or choppiness instead.
- Comparison: the share of the rise from many small gains against the share from the few biggest hours -> replaced: neither part of the split can be computed from catalogue components.
- Outcome: the coin keeps rising over the next 3 days (72 bars) -> kept.
- Verdict transfer: no: a test built on R-squared or efficiency ratio would judge path smoothness, not how much of the rise came from the biggest hours, so its verdict would not carry to the idea.
Reason: The idea needs, for one coin's closes over the last 72 hourly bars, the share of the 3-day rise made by its few largest hourly gains. No catalogue component, alone or combined by weights, offsets or transforms, splits a window's return by the size rank of its one-bar moves. Efficiency ratio, R-squared and variance ratio measure other properties of the path. A jump in an otherwise quiet window still gives a high efficiency ratio, and a high R-squared when the jump comes early or late.
