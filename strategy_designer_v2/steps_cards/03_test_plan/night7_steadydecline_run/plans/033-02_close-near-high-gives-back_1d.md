---
idea: 033-02_close-near-high-gives-back
brief: 033_close-location-next-day-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: the daily close's position within that day's high-low range, graded (the nearer the high, the stronger) -> kept
- Comparison: none (graded across the range, no reference level) -> kept
- Outcome: the price falls over the next day, more the nearer the close was to the high -> kept
- Verdict transfer: yes: the forecast is a short sized by the close's position in the range (0 at the low, largest at the high), so the next-day result answers the idea either way.
Forecast: The only indicator is the close's position in the day's range, CloseLocationInRangeComponent with reference "low": (close − low) / (high − low), from 0 at the low to 1 at the high. It is standardised over its past 60 values (min_periods 20), which gives about 10 for a usual position. It is then negated, so the forecast is a short. - Size: the short grows linearly with how near the close sits to the high, from about -20 at the high (capped) to 0 at the low. - Sign: it is never long, and it is zero only when the close is at the day's low. - No regime: the idea is graded across the whole range, so every bar is active.
Config: 033-02_close-near-high-gives-back_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The least-squares slope of the coin's next-day return, minus the coin's mean daily return over all its windows, on the close's position in the range (close_loc last_history_value). It is pooled over every bar of every coin and window, with no return computed across two windows. Its t treats each day's cases on several coins as one piece of evidence.
- Supporting check: The mean next-day return minus the coin's mean, over bars whose close location is in the top fifth (≥ 0.8), is below 0 (a fall, not only a weaker day).
- Confirm: The slope is negative with t ≤ -2, and the supporting check passes.
- Reject: The slope is positive with t ≥ +2 (closes near the high are followed by higher next days than closes near the low).
- Inconclusive: Any slope with |t| < 2, or a slope with t ≤ -2 whose top-fifth mean is not below 0. At least 500 distinct days of cases and at least 300 bars in the top fifth are required, else inconclusive.
