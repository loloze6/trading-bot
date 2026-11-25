---
idea: 041-01_wide-up-day-next-day-fade
brief: 041_wide-range-days-reverse-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: an up-closing day, graded by its high-to-low range in units of its 30-day daily-return swing -> replaced: the catalogue has no range-over-return-std component; only range over mean bar range (`RangeCompressionRatioComponent`) or over its own past range (`standardise`).
- Comparison: the range against the coin's 30-day daily-return standard deviation -> replaced: by the mean bar range, a different denominator.
- Outcome: the coin falls over the next day, more for wider ranges -> kept: a short forecast held 1 bar.
- Verdict transfer: no: a test on range in mean-bar-range units would not confirm or reject a claim about range in return-swing units.
Reason: The up-close condition fits a regime rule, and the next-day short fits the config. But no component, alone or combined, divides a day's high-to-low range by the standard deviation of the last 30 daily returns. `vol_normalize` uses the 24-bar price standard deviation, and the range components divide by mean bar ranges.
