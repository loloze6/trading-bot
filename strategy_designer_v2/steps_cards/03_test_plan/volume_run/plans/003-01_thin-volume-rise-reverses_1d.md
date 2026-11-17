---
idea: 003-01_thin-volume-rise-reverses
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin rises sharply over one day on volume well below its own 30-day average -> adapted: the rise's size is graded with a strong dead zone, and "well below" is a regime on volume / 30-day average of 0.75 or less.
- Comparison: the larger the rise and the thinner the volume against the 30-day average, the larger the giveback -> adapted: the rise is graded continuously, and thinness is graded in two volume bands (0.5 or less, and above 0.5 up to 0.75).
- Outcome: the price gives back part of the rise over the next 5 days -> adapted: "after X" becomes "while X", so the short is held only on the signal bar, and the 5-day return is measured in the record.
- Verdict transfer: yes: the test measures the same thin-volume rises against the same 5-day giveback, so a confirm or a reject carries over to the idea.
Forecast: The forecast is short only, and only on days with thin volume. Volume is measured as the day's volume over its 30-day average (VolumeRatio, period 30). - Very thin (ratio 0.5 or less, regime mean_reversion). The rise is the day's return in units of the coin's usual daily move (VolatilityScaledReturn, period 1, vol_period 20). It is standardised over 60 bars and clipped at 0, so only rises count. It then goes through signed_power with exponent 3 and pivot 10, and is negated. - A rise of the usual size gives about -10. - A sharp rise reaches the -20 cap. - A small rise gives nearly 0. - Moderately thin (above 0.5 up to 0.75, regime chop). The forecast is the same, but with pivot 20. This makes it exactly one quarter of the very-thin forecast for the same rise, so thinner volume gives a larger short. - Other days. On any other volume, and on down days, the forecast is 0.
Config: 003-01_thin-volume-rise-reverses_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The event bars are the bars with forecast ≤ -2. Within each window, keep the first event and drop any event less than 5 bars after a kept one, so the 5-day returns do not overlap. For each event, take the 5-bar return close[t+5]/close[t] - 1 inside the window, minus the coin's mean 5-bar return over all windows on the non-overlapping grid. The measure is the mean of this excess return, with its t.
- Supporting check: Split the events at the median of |forecast|. The mean excess return of the larger half, minus that of the smaller half, must be ≤ 0.
- Confirm: The idea is confirmed when the mean excess return is ≤ 0 with t ≤ -2, on at least 30 events, and the supporting check passes.
- Reject: The idea is rejected when the mean excess return is ≥ 0 with t ≥ +2, on at least 30 events.
- Inconclusive: These results neither confirm nor reject: - a t between -2 and +2; - t ≤ -2 but the supporting check fails; - fewer than 30 non-overlapping events.
