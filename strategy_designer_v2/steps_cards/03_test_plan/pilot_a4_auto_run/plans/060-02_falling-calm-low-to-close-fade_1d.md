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
- Situation: in falling calm market, close far above the low against the 30-day daily swing -> adapted: a regime with the profile (added by code), plus a score-mode rule that holds (close - low) / close / s30 at 2 or more. The score is the equal-weight mean of CloseOffMidRange and RangeInReturnStd, and it is exact.
- Comparison: the distance from close to low measured in the 30-day standard deviation of daily returns, graded by its size -> replaced: the forecast must standardise each component separately, so their mix weights them by their own past sizes. That mix is not (close - low) / close / s30.
- Outcome: the price falls over the next day, more the further the close stands above the low -> kept: a short held 1 bar.
- Verdict transfer: no: the position would be sized by a different blend of range and close location than the distance the idea grades by, so a reject would not reject the idea.
Reason: The regime can hold the situation exactly, using a score-mode mean of two components. The graded short cannot. `standardise` must come first on each component, and that breaks the exact sum. No single catalogue component outputs the close's height above the day's low in 30-day return standard deviations.
