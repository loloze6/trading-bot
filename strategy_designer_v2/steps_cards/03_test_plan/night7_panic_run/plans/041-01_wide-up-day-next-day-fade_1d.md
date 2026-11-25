---
idea: 041-01_wide-up-day-next-day-fade
brief: 041_wide-range-days-reverse-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a day that closed up, with a wide high-to-low range -> adapted: "after an up-closing day" becomes "while bar t closed up", a regime; inside it the position is graded by the range.
- Comparison: the range in units of the coin's 30-day daily-return swing -> kept: (high - low) / close / std of the last 30 daily returns.
- Outcome: the coin falls over the next day, more so the wider the range -> kept: short for 1 bar, sized by the swing-scaled range.
- Verdict transfer: yes: the book is short only after up days, sized by the range in swing units, so its next-day gains test the claimed fall and its growth with the range.
Forecast: A regime rule sends a bar to `mean_reversion` only when the day closed up, meaning its 1-bar return is above 0. Every other bar is `unknown`, which is flat. Inside the regime, the forecast comes from `RangeInReturnStdComponent` (vol_period 30). This is the day's range over the close, divided by the standard deviation of the last 30 daily returns. It is standardised over the past 60 values (min_periods 20), then negated. So the forecast is always negative on up days: a short of about -10 for a range of usual width, up to -20 for very wide ranges, and near 0 for very narrow ones. It is 0 on every bar that did not close up.
Config: 041-01_wide-up-day-next-day-fade_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The cases are bars with a negative forecast, one per bar. For each case, take the next-day return minus the coin's mean daily return over all windows, in the short direction. Compute its mean over the cases, with its t (cases on the same day summed into one).
- Supporting check: Split the cases into thirds by abs(forecast). The mean unusual move of the top third minus that of the bottom third must be above 0.
- Confirm: The mean unusual move has t >= 2 and the top-minus-bottom-third difference is above 0.
- Reject: The mean unusual move has t <= -2, meaning the next day rises above drift after up days.
- Inconclusive: A t between -2 and 2 is inconclusive. So is a t >= 2 when the top third does not beat the bottom third. At least 300 cases falling on at least 200 distinct days are required, else inconclusive.
