---
idea: 015-04_falls-enlarge-later-returns
brief: 015_directional-volatility-asymmetry-question
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the size of a coin's 1-day fall -> kept: the 1-day return, signed, as `PriceEvolutionComponent` with `period` 1.
- Comparison: the increase after a 1-day rise of the same size -> kept: the same signed 1-day return, which covers the rise side too.
- Outcome: larger absolute daily close-to-close returns over the next 7 days -> replaced: a long or short position in the coin only earns from the price's direction, never from the size of its moves.
- Verdict transfer: no: the claim is about later volatility, not direction, so a position's gains or losses say nothing about it.
Reason: The outcome is the absolute size of the next 7 daily returns, whichever way they go. A config can only hold a long or short position of size forecast / 10 in the coin itself, and it has no volatility position such as a straddle. So no forecast's gains can show whether falls raise later volatility more than equal rises.
