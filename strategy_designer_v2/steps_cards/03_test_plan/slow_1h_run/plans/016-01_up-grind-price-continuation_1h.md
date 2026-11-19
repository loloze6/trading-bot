---
idea: 016-01_up-grind-price-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: coin has risen over the past 3 days (72 bars) -> kept: a regime rule on the 72-bar return above 0, or a component that is 0 when the window did not rise.
- Comparison: share of the rise made by many small hourly gains rather than its few biggest hours -> replaced: no catalogue component grades this share.
- Outcome: the coin keeps rising more over the next 3 days (72 bars) -> kept.
- Verdict transfer: no: the only graded stand-ins measure something else, so a result would not say whether the share itself predicts continuation.
Reason: `TopGainsShareOfRiseComponent` gives the share carried by the top hours, but its complement (1 minus that share) needs a constant offset. A constant inside the "risen" regime makes the position jump, and without the regime the not-risen bars become longs. `RiseBeyondLargestMovesComponent` is the rise times the grind share, which mixes in the rise's size, and the brief says size must be kept apart from how the move was built.
