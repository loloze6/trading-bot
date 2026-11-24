---
idea: 031-04_down-streak-length-continuation
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8342b7be17d6
---
Fidelity:
- Situation: the coin has closed lower several days in a row -> kept: the current run of lower closes, counted in bars (`UpCloseStreakLengthComponent`, side "down").
- Comparison: the run's length against the coin's own down-close streaks over the past 365 days -> kept: the run length divided by the mean length of the completed down streaks in the last 365 bars (base "mean_streak").
- Outcome: the more unusual the run, the more the price keeps falling over the next 5 days -> kept: a short position that grows with that ratio and is held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own ratio, signed short, held for its 5-day horizon, so a confirm or a reject of the short's excess return speaks directly to the idea.
Forecast: The current down-close streak length n is divided by the mean length of the coin's completed down streaks over the last 365 daily bars. It is standardised over its own past 365 values and negated. The forecast is 0 on any bar that did not close lower. It is negative (short) on a down close, and grows in size with how long the streak is against the coin's usual streak, up to the cap of -20. It never goes long.
Config: 031-04_down-streak-length-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are short bets: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, in the short direction. Report its mean and its t, with cases on the same day summed into one.
- Supporting check: Split the cases at the median of |forecast|. The mean short-direction unusual move of the larger half must exceed that of the smaller half: the size of the fall grows with the streak's unusualness.
- Confirm: The main measure's mean is positive with t ≥ 2 over at least 30 distinct days, and the supporting check passes.
- Reject: The main measure's mean is negative with t ≤ -2 over at least 30 distinct days: down streaks are followed by rises beyond the drift.
- Inconclusive: Any t between -2 and 2, or a confirming t whose supporting check fails, or fewer than 30 distinct case days.
