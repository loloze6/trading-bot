---
idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: 30-day hourly volatility low against its own last 6 months, plus the weekend move from Saturday 00:00 to Monday 00:00 UTC -> kept: a regime rule makes the bar closing at Monday 00:00 active only when 720-bar volatility is below its 4320-bar mean, and the forecast is the 48-bar return on that bar.
- Comparison: the larger the weekend move, the larger the continuation -> kept: the position is graded by the standardised size of the weekend move.
- Outcome: the price continues in the weekend's direction over Monday and Tuesday -> kept: each bet is held 48 bars from Monday 00:00.
- Verdict transfer: yes: the test bets on exactly the weekend move, in calm weeks only, over exactly Monday and Tuesday.
Forecast: The forecast is not zero on one bar a week: the bar closing at Monday 00:00 UTC (the coming bar is Monday, hour 0), and only when the coin's 720-bar (30-day) volatility of hourly returns is at or below its mean over the last 4320 bars (6 months). On that bar the forecast is the 48-bar percent return (Saturday 00:00 to Monday 00:00 closes), standardised against its last 60 values. It is long after a weekend rise and short after a weekend fall, and it grows linearly with the move's size, capped at ±20. On every other bar the forecast is 0. The holding period keeps the bet through Monday and Tuesday.
Config: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the bets: bars in the trending regime with |forecast| ≥ 2, one per coin per calm week. For each case, take (forecast / 10) × (the coin's 48-bar return from that close, minus the coin's mean 48-bar return over all its windows). The measure is the mean of this value over the cases, with its t of the mean, before costs.
- Supporting check: none
- Confirm: The mean is positive with t ≥ 2 over at least 100 cases.
- Reject: The mean is negative with t ≤ -2 over at least 100 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 100 cases with a full 48 bars left inside their window, is neither a confirm nor a reject.
