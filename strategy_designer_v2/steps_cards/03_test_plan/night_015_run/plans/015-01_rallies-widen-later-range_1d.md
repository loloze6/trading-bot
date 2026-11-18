---
idea: 015-01_rallies-widen-later-range
brief: 015_directional-volatility-asymmetry-question
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the size of a coin's 1-day rise -> kept: graded 1-bar return (PriceEvolutionComponent, period 1).
- Comparison: against a 1-day fall of the same size -> kept: the same signed 1-bar return read on down bars.
- Outcome: a wider average daily high-low range over the next 7 days, in no direction -> replaced: a config only sets a long or short position, which gains from the price's direction, not from its range.
- Verdict transfer: no: a directional result neither confirms nor rejects a claim about the size of later ranges.
Reason: The idea's outcome is later volatility (the 7-day average high-low range), not a price direction. A spot long or short position set by the forecast gains only from direction, so no config can bet on range widening. Trading volatility would need instruments such as options or straddles, which the config cannot express.
