---
idea: 003-04_heavy-volume-drop-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp one-day fall on volume well above its 30-day average -> kept: a one-day fall of at least 2 usual daily moves on volume of at least 1.5 times its 30-day mean is the regime condition, and the position size grows with both.
- Comparison: the bar's volume against its own 30-day average daily volume -> kept: VolumeRatioComponent over 30 bars, used as the gate and as a graded size term.
- Outcome: keeps falling over the next 5 days, more after larger and heavier falls -> adapted: holding period dropped; the short lasts only while the situation lasts, and the 5-day loss is measured from the recorded closes.
- Verdict transfer: yes: the test reads the 5-bar return after the same heavy-volume sharp falls, and checks that it grows with the forecast's size.
Forecast: Two measures are computed on every bar: - the current day's return in usual moves (VolatilityScaledReturnComponent, period 1, 20-bar volatility); - the day's volume over its 30-day mean (VolumeRatioComponent, period 30). The regime is active only when the return is at or below -2 usual moves and the volume ratio is at or above 1.5. On every other bar the forecast is zero. When the regime is active, the forecast is the equal-weight mean of two parts: - the standardised return (negative, larger with a bigger fall); - the standardised volume ratio, negated (negative, larger with heavier volume). Both are standardised over the past 60 bars and capped at ±20, and the result is clipped at 0. So the forecast is short only, and it grows with both the fall and the volume.
Config: 003-04_heavy-volume-drop-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On signal bars (forecast < 0), take the 5-bar return close[t+5]/close[t]-1 inside the window, minus the coin's mean 5-bar return over all windows (holding the coin). Use non-overlapping events only: within a window, skip a signal that falls within 5 bars of the previous one kept. Report the t of the mean excess return and the number of events.
- Supporting check: Split the events at the median forecast. The mean excess 5-bar return of the half with the more negative forecasts, minus that of the other half, must be below 0.
- Confirm: The mean excess 5-bar return is negative with t ≤ -2 over at least 30 independent events, and the supporting check passes.
- Reject: The mean excess 5-bar return is positive with t ≥ +2 over at least 30 independent events, meaning heavy-volume falls are followed by gains beyond holding the coin.
- Inconclusive: Any t between -2 and +2, a confirming t whose supporting check fails, or fewer than 30 independent events.
