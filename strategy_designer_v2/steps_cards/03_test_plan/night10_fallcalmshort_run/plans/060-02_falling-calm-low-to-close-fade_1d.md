---
idea: 060-02_falling-calm-low-to-close-fade
brief: 060_falling-calm-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, calm market, a day closing far above its low against the 30-day daily swing -> replaced: no component gives (close − low) / close over the 30-day std of daily returns; the nearest are a mean-bar-range base or a mix of two components whose standardised weights drift.
- Comparison: the close's height above the low, against the coin's 30-day daily swing -> replaced: the same gap as above.
- Outcome: a fall over the next day, larger the further the close stands above the low -> kept: a short graded by that height, held 1 bar.
- Verdict transfer: no: a test on mean bar ranges or on a drifting mix of two components measures a different height, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea's measure is the close's height above the day's low in units of the 30-day std of daily returns. The closest single component is `BreakoutInMeanRangesComponent` with `extreme` "low", which divides by the mean bar range, not the return swing. The exact sum `RangeInReturnStdComponent` + `VolatilityScaledDistanceFromHighComponent` (period 1, high, base close) cannot be kept, because `standardise` rescales each part by its own past mean, so the mix drifts.
