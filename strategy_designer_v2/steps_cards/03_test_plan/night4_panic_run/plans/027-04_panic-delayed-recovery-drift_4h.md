---
idea: 027-04_panic-delayed-recovery-drift
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch where the range is several times its usual size and the price falls hard -> replaced: no catalogue component measures the range of a stretch that ended one day ago; only the lagged close-to-close fall (`VolatilityScaledReturnComponent`, `lag`) exists.
- Comparison: the later return against the coin's usual return, larger as the panic is more extreme -> kept: return against holding the coin, graded by panic size.
- Outcome: the return from 1 day to 14 days after the stretch ends is higher -> kept: the situation lagged 6 bars, then held 78 bars (4h bars).
- Verdict transfer: no: a test on the lagged fall alone drops the range condition, so its verdict would not be about panic stretches as the idea defines them.
Reason: The return starts one day after the stretch ends, so the panic must be read 6 bars late, and the catalogue has no lagged range measure. It has only a lagged close-to-close fall, and a weighted mean cannot require a large range and a hard fall together. Both parts are in the coin's own high, low and close, so one lagged component could hold them.
