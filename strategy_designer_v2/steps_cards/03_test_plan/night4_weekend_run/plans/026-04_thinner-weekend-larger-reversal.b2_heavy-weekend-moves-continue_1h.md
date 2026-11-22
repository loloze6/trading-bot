---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the Saturday-Sunday move, on weekend volume higher than the mean of the preceding five weekdays, larger move and heavier volume counting more -> kept: at Sunday 23:00 the 48-bar move, gated by the 48-bar volume over the prior 120-bar volume, graded by both.
- Comparison: weekend volume against the mean volume of the preceding five weekdays -> kept
- Outcome: price continues in the weekend move's direction over the next 48 hours -> kept
- Verdict transfer: yes: the forecast bets in the weekend move's direction for 48 bars only after heavy-volume weekends, sized by the move and the volume, so its result answers the idea.
Forecast: Only on the bar whose next bar opens Monday 00:00 UTC, and only when the mean volume of the last 48 hours is above the mean of the 120 hours before them, the forecast follows the weekend's 48-bar move. It is the weighted mean of two parts. The first part has weight 2: the 48-bar return in usual 48-bar moves, standardised. The second part has weight -1: the same return times the prior five days' mean volume over the weekend's mean volume, standardised. Together this is about the return x (2 - weekday/weekend volume). The forecast is positive after a weekend rise and negative after a weekend fall. It grows with the size of the move and as the weekend volume gets heavier than the weekdays' volume. It is zero on every other bar. The 48-bar hold keeps each bet through Monday and Tuesday.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Measured on each case, one per qualifying Sunday 23:00 bar with a non-zero forecast. The value is the coin's return over the next 48 bars minus the coin's mean 48-bar return over all its windows, times the sign of the forecast. The measure is the t of its mean over all coins and windows.
- Supporting check: The mean signed unusual move of the cases in the top half of |forecast| minus that of the bottom half is above 0.
- Confirm: The main t is 2 or more over at least 100 cases, and the supporting difference is above 0.
- Reject: The main t is -2 or less over at least 100 cases, meaning heavy-volume weekend moves are reversed.
- Inconclusive: A main t between -2 and 2, or a t of 2 or more with the check failing. Any result with fewer than 100 cases is also inconclusive.
