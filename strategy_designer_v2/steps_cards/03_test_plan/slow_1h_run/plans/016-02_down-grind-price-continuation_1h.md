---
idea: 016-02_down-grind-price-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has fallen over the past 3 days (72 bars) -> kept
- Comparison: share of the fall made by many small hourly losses rather than by its few biggest hours -> replaced: no catalogue component measures how concentrated the fall is in its largest hours
- Outcome: the coin keeps falling over the next 3 days (72 bars), more the larger that share -> kept
- Verdict transfer: no: efficiency ratio or R-squared measure straightness, not concentration in the biggest hours, so a verdict would not transfer.
Reason: The idea's grind-versus-jump split needs the share of a 72-bar fall made by its few largest hourly losses. No component, alone or combined, computes this. The candidate stand-ins (EfficiencyRatioRegimeComponent, RSquaredRegimeComponent, VolatilityRankedFallComponent) measure path straightness or a single bar's move. The data needed is in each coin's own closes, and the config's logic could hold it as a graded component.
