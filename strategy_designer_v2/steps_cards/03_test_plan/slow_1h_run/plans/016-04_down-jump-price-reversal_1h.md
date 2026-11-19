---
idea: 016-04_down-jump-price-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has fallen over the past 3 days -> adapted: graded size of the 72-bar fall, held while it lasts (PriceEvolutionComponent, period 72).
- Comparison: the larger the share of that fall made by its few biggest hourly losses -> replaced: no catalogue component, alone or combined, measures how much of a 72-bar fall its largest one-bar losses made.
- Outcome: the coin wins back more of the fall over the next 3 days (up) -> kept: a long position graded by the share, judged on the 72-bar return after it.
- Verdict transfer: no: without the share of the fall made by the biggest hours, the test would only measure fall size, which the brief says the idea must go beyond.
Reason: The idea needs the share of a 72-hour fall that came from its few largest hourly losses. That uses only one coin's own closes and fits a graded forecast, but no catalogue component computes it. Efficiency ratio, volatility-scaled or ranked one-bar falls, and range or volume ratios measure path smoothness or a single bar, not how concentrated a multi-bar fall is in its top hours.
