---
idea: 086-01_heavy-volume-up-day-continuation
brief: 086_falling-calm-heavy-volume-rise-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling calm market, a day closing up on volume heavy against its 20-day average -> adapted: the profile is added by code; "up close and volume above its prior 20-day mean" is a regime, and inside it the position grows with the volume's excess.
- Comparison: the heavier the volume against its 20-day average, the larger the rise -> kept: the forecast is graded by the volume ratio minus 1.
- Outcome: a further rise over the next 5 days -> kept: each bet is held for 5 bars, long only.
- Verdict transfer: yes: the test bets on exactly those days, sized by the volume excess, and judges their next 5 days against the coin's drift.
Forecast: A bar is active only when it closes above the previous close and its volume is above the mean of the prior 20 days' volume. On every other bar the forecast is 0. "Heavy" has no number in the idea or the brief, so the level is the convention "above the average". On active bars the forecast is the volume ratio minus 1 (volume over the prior 20-day mean, minus 1), standardised against its own past 60 values and clipped at 0. It is therefore positive (long), near 0 when the volume is just at its average, and larger the heavier the volume, up to the cap of 20. The profile (falling calm) is added by code, and the book is flat outside it.
Config: 086-01_heavy-volume-up-day-continuation_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case (a bet of the forecast, once per 5-bar grid cell). This is the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, with its t (cases of one day taken together).
- Supporting check: The rise must grow with the volume. The Spearman correlation between the case's `heavy_vol` raw value (`last_history_value`) and its unusual move must be above 0.
- Confirm: The mean unusual move is above 0 with t >= 2, and the supporting correlation is above 0.
- Reject: The mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a correlation at or below 0. The test also needs at least 30 cases over the coins and windows; with fewer, the result is inconclusive.
