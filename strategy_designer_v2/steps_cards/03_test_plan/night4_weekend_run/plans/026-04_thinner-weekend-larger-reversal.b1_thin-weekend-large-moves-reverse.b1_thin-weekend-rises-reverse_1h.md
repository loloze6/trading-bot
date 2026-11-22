---
idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: a coin's Saturday-Sunday rise, larger is stronger -> kept: the 48-bar return over the weekend, read on Sunday's last hourly bar, in usual 48-hour moves, short side only when it rose.
- Comparison: weekend volume lower than the mean of the preceding five weekdays, lower is stronger -> kept: a regime rule (weekend mean volume / weekday mean volume < 1), with the weekday-over-weekend volume factor grading the size.
- Outcome: the rise is partly reversed over the next 48 hours (Monday and Tuesday), a fall -> kept: a short opened at Sunday's close and held 48 bars.
- Verdict transfer: yes: the test bets exactly the weekend rise's reversal, sized by the rise and the volume shortfall, only on the qualifying weekends, so a confirm or a reject applies to the idea.
Forecast: The forecast is computed only on the bar whose next bar starts Monday 00:00 UTC (Sunday 23:00), and only when the weekend's mean hourly volume is below the mean of the 120 weekday bars before it. That volume ratio is VolumeRatioComponent with period 120, exclude_current 48 and short_period 48. On that bar the forecast is ThinVolumeScaledReturnComponent with period 48, window 720, volume_period 48, base_near 48 and base_far 167. It is the weekend's 48-hour return in usual 48-hour moves, times the weekday mean volume over the weekend mean volume. It is standardised (window 500, min_periods 120), negated, and clipped at 0. So it is negative (short) only after a weekend rise. Its size grows with the rise and with how thin the weekend was against the week. It is 0 after a weekend fall, on weekends with volume at or above the weekday mean, and on every other bar. The short is held 48 bars.
Config: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is each weekend with a nonzero forecast. For each case, take the coin's return over the 48 bars after the signal bar's close, minus the coin's normal 48-bar drift (holding the coin, all windows), signed in the short direction. Average these unusual moves weighted by |forecast|, with the t over the cases (they do not overlap).
- Supporting check: The mean short-side unusual move of the cases in the larger half of |forecast| is above that of the smaller half (difference > 0).
- Confirm: The weighted mean short-side unusual move is above 0 with t >= 2, and the supporting check passes.
- Reject: The weighted mean short-side unusual move is below 0 with t <= -2, meaning weekend rises are followed by further rises on Monday and Tuesday.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. Fewer than 100 cases over all coins and windows is inconclusive whatever the t.
