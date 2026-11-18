---
idea: 015-02_rallies-enlarge-later-returns
brief: 015_directional-volatility-asymmetry-question
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a coin's 1-day rise, larger is stronger -> kept: VolatilityScaledReturnComponent (period 1) gives the signed one-day move.
- Comparison: against the increase after a 1-day fall of the same size -> kept: the same signed one-day return covers falls of equal size.
- Outcome: larger absolute daily close-to-close returns over the next 7 days, with no direction -> replaced: a spot position gains only from the direction of the price, not from the size of its moves.
- Verdict transfer: no: a directional position's gain cannot show whether later absolute returns grow, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea predicts how large the next 7 days' moves will be, not which way they go. The config can only set a long or short spot position, which gains or loses with the price's direction. The guide lists no way to hold a position that pays on the size of moves in either direction, such as a straddle or volatility exposure. So this outcome is outside what the config can express.
