---
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 21:00 to 23:00 UTC slot, 7-day hourly volatility and the 24-hour fall -> replaced: a regime keeps the slot and the volatility is a graded component, but no component computes volatility times the 24-hour fall.
- Comparison: a larger rise at higher volatility, more so after a larger 24-hour fall -> replaced: a weighted mean can only add volatility and fall, not let the fall amplify the volatility effect.
- Outcome: the coin rises over the two hours from 21:00 to 23:00 UTC -> kept: a long held 2 bars on 1h bars.
- Verdict transfer: no: without the volatility-times-fall interaction the test cannot confirm or reject "the more so the further it fell".
Reason: The slot fits in a regime rule on HourOfDayComponent (between 20.5 and 22.5), and the 168-bar volatility fits VolatilityFromStdDevComponent. The idea's core is an interaction: the volatility effect grows with the 24-hour fall. Weighted means, negative weights, offsets and signed_power can only sum standardised components, and no catalogue component multiplies a multi-bar fall by volatility. VolatilityRankedFallComponent uses only the one-bar fall, and VolatilityScaledReturnComponent divides by volatility.
