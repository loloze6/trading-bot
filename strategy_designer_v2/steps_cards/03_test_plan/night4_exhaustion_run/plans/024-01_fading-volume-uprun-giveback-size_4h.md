---
idea: 024-01_fading-volume-uprun-giveback-size
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin has just risen in an unbroken streak of four-hour bars with fading volume, and the gain is large against its typical 4h move over 30 days -> kept: a veto requires 4 consecutive up bars; another requires the last 2 bars' volume to be below the 4-bar mean; the 4-bar gain is divided by the 180-bar standard deviation of 4h returns.
- Comparison: the streak's gain against the coin's typical four-hour move over the past 30 days -> kept: VolatilityScaledReturnComponent with period 4 and vol_period 180.
- Outcome: the coin falls over the next three days, more after a larger gain -> adapted: a graded short held for 18 bars, sized by the scaled gain while the streak lasts.
- Verdict transfer: yes: the streak, the fading volume, the scaled gain and the 3-day fall are all measured as stated, and only the entry is made graded.
Forecast: The forecast is computed only when two vetoes pass: - the last 4 four-hour bars each closed up; - the mean volume of the last 2 bars is below the mean volume of the last 4 bars, so volume fades across the streak. When both hold, the forecast is short. Its size is the 4-bar gain measured in the coin's 30-day (180-bar) volatility of 4h returns. That value is standardised against its own past 181 values and negated. A larger streak gain against the usual move gives a larger short. On every other bar the forecast is 0. The forecast never goes long. Each bet is held for 3 days.
Config: 024-01_fading-volume-uprun-giveback-size_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the short bets (rises of the short forecast of at least the band). Each case is read once per cell of an 18-bar grid in each window. For each case, take the coin's 18-bar return from the signal bar's close, minus the coin's normal 18-bar drift over all windows, in the short direction. The measure is the mean of these values and its t.
- Supporting check: Split the cases at the median absolute forecast. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean unusual move in the short direction is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move in the short direction is below 0 with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails, and any result with fewer than 30 independent cases.
