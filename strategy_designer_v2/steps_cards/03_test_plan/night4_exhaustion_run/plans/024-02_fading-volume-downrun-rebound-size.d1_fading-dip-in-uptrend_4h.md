---
idea: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars whose volume declined across the streak, while the coin rose over 30 days -> adapted: "just fallen" becomes "while the down-streak lasts"; the fading volume (streak volume slope) and the 30-day rise above 0 are a regime condition.
- Comparison: the streak's loss against the typical 4h move over 30 days, and the size of the 30-day rise -> kept: both are graded components, combined additively so that each one increases the size.
- Outcome: the coin rises over the next three days -> kept: a long position, each bet held 18 bars.
- Verdict transfer: yes: every condition and scale is measured as stated, and only the timing is adapted, which is allowed.
Forecast: The forecast is flat unless two conditions hold at the bar's close. The coin's 180-bar (30-day) return must be above 0. The current down-streak of closes must show fading volume, which means the negated volume slope of DownStreakVolumeFade is above 0. This also requires a streak of at least 2 bars. When both hold, the forecast is long. It is the equal-weight mean of two standardised parts (window 181, min_periods 45): - the streak's summed loss in usual one-bar moves over 180 bars; - the 180-bar percent rise, clipped at 0. The forecast is positive and grows with the depth of the streak's loss and with the size of the 30-day rise. It is never negative, and it is 0 outside the regime.
Config: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet (the forecast rising by at least 2 points), read once per cell of a non-overlapping 18-bar grid in each window. Measure the coin's 18-bar return from the signal bar minus its normal 18-bar drift (taken over all windows). Average these excess returns weighted by the forecast at the signal, pooled over coins, with the t of that mean.
- Supporting check: The book's timing gain must be positive. This is its mean daily return before costs, minus the part due to the market's own rise (position × the coin's mean daily return).
- Confirm: The weighted mean excess return is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The weighted mean excess return is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or a confirming t with a timing gain of 0 or below. Fewer than 30 independent cases is inconclusive whatever the t.
