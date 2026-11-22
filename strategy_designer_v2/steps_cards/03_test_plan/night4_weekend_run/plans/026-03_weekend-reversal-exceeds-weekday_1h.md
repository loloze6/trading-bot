---
idea: 026-03_weekend-reversal-exceeds-weekday
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin's 48-hour return over Saturday and Sunday -> kept: the 48-bar return read at the close of Sunday's last hour (the coming bar is Monday 00:00 UTC).
- Comparison: same-size 48-hour returns ending on other weekdays, reversed less -> kept: weekday 48-hour returns and their next 48 hours, recomputed from the recorded closes and compared per unit of move.
- Outcome: a larger opposite move over the next two days -> kept: the reversal bet is held 48 bars (Monday and Tuesday).
- Verdict transfer: yes: the test measures how much weekend moves reverse against same-size weekday moves, with the idea's own durations and timing.
Forecast: A regime fires on one bar a week only: the bar whose next bar starts Monday 00:00 UTC (weekday 0 and hour 0). On that bar the forecast is minus the standardised 48-bar return, which is Saturday 00:00 to Monday 00:00. The return is standardised over its own last 60 values, about 10 for a usual size and capped at 20. The forecast is short after a weekend rise and long after a weekend fall, and it grows with the size of the weekend move. On every other bar the forecast is 0, and the bet is held for 48 bars.
Config: 026-03_weekend-reversal-exceeds-weekday_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The reversal score compares two groups of cases. Per case, the score is -(past 48h return / usual 48h move) x ((next 48h return - normal 48h drift) / usual 48h move), recomputed from the recorded closes. Weekend cases end at Monday 00:00 UTC. Weekday cases end at Wednesday 00:00 and Friday 00:00 UTC. The measure is the mean score over weekend cases minus the mean over weekday cases, with Welch's t, pooled over coins and windows.
- Supporting check: Weekend reversal exists. Over the weekend cases, take the unusual 48-bar move in the forecast's direction, weighted by |forecast|. It must have a positive mean with t >= 2.
- Confirm: The weekend-minus-weekday difference has Welch t >= 2, and the supporting check passes (t >= 2).
- Reject: Either the weekend-minus-weekday difference has t <= -2, or the weekend cases' unusual move in the forecast's direction has t <= -2.
- Inconclusive: Any other result, including a difference with |t| < 2 or a positive difference whose weekend check fails. At least 300 weekend cases and 300 weekday cases are needed; with fewer, the result is inconclusive.
