---
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the coin falls over the weekend, Saturday 00:00 to Monday 00:00 UTC -> kept: the 48-bar return is read on the bar that closes at Monday 00:00, selected by a regime rule on the coming bar's weekday and hour, and only falls are kept.
- Comparison: the fall is larger the more volatile the weekend's hours were against the coin's previous week -> replaced: no component multiplies the weekend move by that volatility ratio, and a weighted mean can only add the ratio as a separate bet.
- Outcome: the coin keeps falling over Monday and Tuesday (short) -> kept: each bet is held 48 bars from Monday 00:00.
- Verdict transfer: no: adding the volatility ratio instead of letting it scale the fall would short calm-fall and turbulent-rise weekends, so the verdict would not be about the idea's graded claim.
Reason: The weekend fall is kept, and so are its timing (a weekday and hour regime with a 48-bar hold) and the hold over Monday and Tuesday. No catalogue component sizes that fall by the weekend's volatility against the prior week's. The config can only add components, never multiply them. `VolatilityRatioToAverageComponent` and `VolatilityScaledReturnComponent` each compare against a rolling mean that includes the weekend itself, so neither gives the weekend-over-previous-week ratio.
