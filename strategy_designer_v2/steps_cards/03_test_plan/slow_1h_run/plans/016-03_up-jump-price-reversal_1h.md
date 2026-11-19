---
idea: 016-03_up-jump-price-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has risen over the past 3 days, and a share of that rise came from its few biggest hourly gains -> replaced: no catalogue component measures how concentrated a rise is in its largest hours.
- Comparison: a larger share from the biggest hours against a smaller share -> kept: the forecast's size would grow with the share.
- Outcome: the coin gives back more of the rise over the next 3 days (72 bars), a fall -> kept: a short position that grows with the share, held while the situation holds.
- Verdict transfer: no: a stand-in for the concentration (ER, volatility, range) would test a different quantity, so a result would not transfer to the idea.
Reason: The 72-bar rise is available (`PriceEvolutionComponent`, period 72), but no component computes the share of that rise carried by its largest hourly gains. I tried the guide's compositions: efficiency ratio, return volatility, Donchian or range position, `VolatilityScaledReturnComponent` and `VolumeWeightedScaledReturnComponent`. None of them, alone or combined, isolates the top hourly gains inside the window; each measures dispersion or path, not concentration. The quantity needs only the coin's own closes, and the config's logic could hold it as a graded component, gated by the rise.
