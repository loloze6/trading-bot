---
idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the 3-day return is high against the coin's typical move over the past 30 days -> kept: the 18-bar return divided by the mean absolute 18-bar return over 180 bars, long side only.
- Comparison: the effect is stronger when the 30-day volatility is low than when it is high -> kept: the criterion compares the effect on low-volatility cases with high-volatility cases, recomputed from closes.
- Outcome: the coin rises further over the next three days, more for a higher scaled return -> kept: the 18-bar forward return against the coin's drift, graded by the forecast.
- Verdict transfer: yes: the forecast is the idea's scaled return, and the criterion tests both the graded rise and its stronger form in calm markets.
Forecast: The 3-day (18-bar) return is divided by the mean absolute 18-bar return over the last 30 days (180 bars). This uses MeanAbsScaledReturnComponent with period 18 and window 180. The result is standardised against its own past 198 values and clipped at 0. The forecast is 0 when the 3-day return is flat or negative. It is positive and grows in proportion as the 3-day advance gets larger against the coin's usual 3-day move: about +10 for an advance of the usual size, capped at +20. It is long only and never negative.
Config: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The slope of the coin's next-18-bar return, minus its mean 18-bar return over all windows, regressed on the forecast. It is measured at the non-overlapping 18-bar grid bars of each window, pooled over coins and windows, with the t of the slope.
- Supporting check: The grid cases are split by the coin's 30-day volatility, recomputed from closes as the std of 4h returns over 180 bars. The split is at that coin's median over all its windows. The slope on the low-volatility half must exceed the slope on the high-volatility half (difference low minus high > 0).
- Confirm: The main slope is positive with t ≥ 2, and the low-volatility slope exceeds the high-volatility slope.
- Reject: The main slope is negative with t ≤ -2.
- Inconclusive: The idea is inconclusive in two cases. Either the main slope has t between -2 and 2, or the main t is ≥ 2 but the low-volatility slope does not exceed the high-volatility one. At least 100 grid cases with a forecast above 0 are needed in total, and at least 30 in each volatility half; with fewer, the result is inconclusive.
