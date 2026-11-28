---
idea: 086-01_upper-shadow-further-fall
brief: 086_falling-agitated-rejected-rally-wick
data-instruments: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, agitated market, a day's upper shadow (high above the higher of open and close) -> replaced: no catalogue component measures high minus max(open, close); only the lower wick and distances from the high to the close exist
- Comparison: the shadow against the coin's usual daily range over the past 30 days -> kept: a 30-bar mean of high minus low is available as a divisor (for example, the base of `BreakoutInMeanRangesComponent`)
- Outcome: a larger fall over the next 3 days, the longer the shadow -> kept: short, graded by the shadow, held 3 bars on 1d bars
- Verdict transfer: no: using the close's distance below the high instead counts a down day's body as shadow, and the brief itself separates the rejected rise from a low close
Reason: The upper shadow needs the bar's open: high minus max(open, close). No component outputs it. The nearest ones, `CloseLocationInRangeComponent` "high", `VolatilityScaledDistanceFromHighComponent` and `BreakoutInMeanRangesComponent` "below", measure high minus close, which includes the down body. The weighted mean of standardised components cannot subtract raw values to remove that body.
