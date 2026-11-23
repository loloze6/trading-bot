---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: Sunday's 24-hour return, scaled by the usual 30-day move and capped near two usual moves, times the coin's 30-day hourly volatility -> replaced: no component or composition multiplies the capped scaled return by hourly volatility; only the raw return or the unweighted scaled return is available.
- Comparison: the Sunday return against the coin's usual 30-day 24-hour move -> kept: `MeanAbsScaledReturnComponent` (period 24, window 720), read on the bar whose coming bar is Monday 00:00 UTC through a weekday and hour regime.
- Outcome: an opposite move over the next 48 hours, growing with that product -> kept: `negate`, with each bet held 48 bars.
- Verdict transfer: no: a test without the volatility weight and the cap measures a different sizing, so it would neither confirm nor reject the stated product.
Reason: The weighted mean of the config can only add components, and score_product mode only gates a regime. So no config can multiply the scaled Sunday move, capped at about two usual moves, by the coin's 30-day hourly volatility. Every input is in the coin's own closes, and the Sunday timing fits a `WeekdayComponent` and `HourOfDayComponent` regime with a 48-bar hold. Only the product itself is missing.
