---
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: one hour's rise far above the typical hourly move, on volume near its 30-day hourly average -> adapted: the rise is graded in multiples of the 30-day mean absolute hourly move, and "after that hour" becomes "at that hour's close"; volume near average is a regime band (0.5 to 1.5 times the 720-bar mean).
- Comparison: the rise against the typical hourly move over 30 days, and volume against average hourly volume over 30 days -> kept: both are measured over 720 bars.
- Outcome: the price gives back part of the rise over the next six hours, more so for larger rises -> kept: the position is short, held 6 bars, and grows with the rise's size in usual moves.
- Verdict transfer: yes: the forecast is short exactly on quiet-volume hourly rises, sized by their multiple of the typical move, and held for the six hours the idea names.
Forecast: The forecast uses MeanAbsScaledReturnComponent (period 1, window 720): this hour's return divided by the mean absolute hourly return of the past 720 bars (30 days). - Scaling. The value is standardised over its past 500 values (min_periods 120), so a typical-size move reads about 10, capped at 20. - Rises only. It is clipped at 0, so only rises count. - Dead zone. It then goes through signed_power (exponent 3, pivot 20), the strongest graded dead zone the guide allows. An ordinary rise maps to about 2.5, 1.5 times the usual standardised size to about 8.4, and twice it or more to 20. - Direction. It is negated, so the forecast is short and grows with the size of the rise. - When it is zero. It is zero on falling or flat hours. The rise saturates at about twice its usual size, so differences among the very largest rises are not graded. - Volume condition. The forecast is active only in the regime where this hour's volume is between 0.5 and 1.5 times its 720-bar mean ("near average"). Elsewhere the regime is null and the book is flat. - Sign. The forecast is never positive.
Config: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The cases are the short bets: the forecast falls by at least 2 points. Each case is read once per cell of a non-overlapping 6-bar grid in each window. For each case, take the coin's return from that bar's close to 6 bars later and subtract the coin's mean 6-bar return over all windows. Sign it short, so a giveback counts positive. The measure is the mean of this unusual move, with its t over the independent cases.
- Supporting check: Split the cases at the median absolute forecast at entry. The mean unusual move of the larger-forecast half, minus that of the smaller half, must be at least 0.
- Confirm: The idea is confirmed when the mean short-signed unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The idea is rejected when the mean short-signed unusual move is negative with t <= -2 over at least 30 cases, meaning the price keeps rising after quiet-volume spikes.
- Inconclusive: Results are inconclusive in these cases: - t is between -2 and 2; - t >= 2 but the larger-rise half shows a smaller giveback than the smaller-rise half; - there are fewer than 30 cases across both coins and all windows.
