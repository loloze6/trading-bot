---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d1_sunday-reversal-grows-with-volatility
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: Sunday's 24-hour return against the coin's usual 30-day move, read at Monday 00:00 UTC -> kept: `MeanAbsScaledReturnComponent` (24, 720) on the one bar a weekday and hour rule selects.
- Comparison: the higher the hourly volatility over the last 30 days, the larger the reversal -> replaced: no component multiplies the scaled return by the hourly volatility, so only the raw 24-hour return could stand in for it.
- Outcome: an opposite move over Monday and Tuesday (48 bars) -> kept: a contrarian bet held for 48 bars.
- Verdict transfer: no: without the volatility product, a test could not tell whether the reversal grows with the coin's turbulence.
Reason: The config combines components only by a weighted mean, and a regime cannot size a bet, so it cannot multiply Sunday's scaled 24-hour return by the 30-day hourly volatility. No catalogue component computes that product. The nearest ones normalise by volatility, use a volatility ratio, or use the raw return, which swaps the hourly volatility for the usual daily move.
