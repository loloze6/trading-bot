---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a Saturday-Sunday move, larger and on heavier volume -> kept: at Sunday 23:00's close, the 48h return in usual 48h moves times the weekend volume over the prior five weekdays.
- Comparison: weekend volume above its mean over the preceding five weekdays, and the move going the same way as the 30-day return before the weekend -> kept: regime rules (volume ratio >= 1, same signs), and the lagged 30-day return adds to the size.
- Outcome: the move continues in the same direction over the next 48 hours -> kept: the bet is held 48 bars.
- Verdict transfer: yes: the test bets exactly on the qualifying weekends and their 48h continuation, so its result is the idea's result.
Forecast: Only one bar a week can carry a forecast: the bar whose next bar starts Monday 00:00 UTC. Four conditions must all hold on that bar: - the coming bar starts Monday at hour 0; - the mean volume of the last 48 bars is at least the mean of the 120 weekday bars before them; - the 48-bar weekend return is above zero, or below zero; - the 30-day return ending at Friday's close (the 720-bar volatility-scaled return, lagged 48 bars) has that same sign. The forecast is the equal-weight mean of two standardised components (window 500, min_periods 120): - A: the weekend 48h return in usual 48h moves (30-day base) times the weekend-to-weekday volume ratio; - B: the 30-day pre-weekend return in usual moves. Inside the regime A and B have the same sign, so the forecast follows the weekend move. It grows with the size of the move, the heaviness of the volume and the strength of the aligned trend. It is zero on every other bar. The bet is held 48 bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is each bar with a non-zero forecast, which is one per qualifying weekend, so the cases do not overlap. Per case, take the coin's 48-bar return from that bar's close, minus the coin's normal 48-bar drift (over all its windows), signed by the forecast's sign. Measure the mean over all cases, with its t.
- Supporting check: The mean signed unusual move of the cases in the top half of |forecast| is above that of the bottom half.
- Confirm: The mean signed unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean signed unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the check failing. A test with fewer than 100 cases over all coins and windows is inconclusive whatever its t.
