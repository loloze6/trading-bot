---
idea: 015-03_falls-widen-later-range
brief: 015_directional-volatility-asymmetry-question
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the size of a coin's 1-day fall -> kept: the 1-bar return, negated, as with `PriceEvolutionComponent` at period 1.
- Comparison: against a 1-day rise of the same size -> kept: the same signed 1-bar return read on up bars.
- Outcome: a wider average daily high-low range over the next 7 days, larger after falls -> replaced: a position can only earn from the price's direction, not from how wide later bars swing.
- Verdict transfer: no: the idea predicts no direction, so a gain or loss on a long or short position says nothing about later range widening.
Reason: The idea's outcome is later volatility (the 7-bar mean high-low range), and it predicts no price direction. The config can only hold a long or short position that gains or loses with the price's direction, so no forecast can be scored on whether ranges widen more after falls than after equal rises.
