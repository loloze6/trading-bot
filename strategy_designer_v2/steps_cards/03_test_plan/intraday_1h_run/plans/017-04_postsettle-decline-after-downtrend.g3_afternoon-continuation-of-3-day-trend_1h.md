---
idea: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: the 2 hours from 16:00 UTC, with the coin's 3-day move -> kept: a clock regime on coming bars 16:00 and 17:00 UTC, plus the 72-bar return.
- Comparison: a stronger 3-day rise goes with a larger 2-hour rise -> kept: the position grows with the size of the 72-bar return.
- Outcome: the 2-hour return from 16:00 follows the 3-day move's direction -> kept: long after a 3-day rise and short after a 3-day fall, held over the bars of 16:00 and 17:00.
- Verdict transfer: yes: the test bets only in that 2-hour slot, in the 3-day direction, sized by its strength, so a significant gain or loss there answers the idea.
Forecast: The forecast is active only on bars whose coming bar starts at 16:00 or 17:00 UTC. The `HourOfDayComponent` rule selects coming hours 16 and 17, so the position is opened at the 16:00 close and held to the 18:00 close. Every other bar is flat. Inside the slot, the forecast is the coin's 72-bar (3-day) percent return, standardised against its own past 73 values (min_periods 20). It is positive after a 3-day rise and negative after a 3-day fall. Its size grows in proportion to the move, about ±10 for a usual 3-day move and capped at ±20. It is 0 only when the 3-day return is 0.
Config: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the bars where the 16:00 slot opens, one per day; the 15:00-stamped bar closes at 16:00. For each case, take forecast/10 × (close[t+2]/close[t] − 1 minus the coin's mean 2-bar return over all its windows). Pool the cases across coins and windows and compute the ordinary t of their mean, before costs.
- Supporting check: Rank the cases by |forecast| and compare the top third with the bottom third. The mean excess 2-bar return signed by the forecast must be larger in the top third (Welch t ≥ 1).
- Confirm: The idea is confirmed when both hold: - the main mean is above 0 with t ≥ 2; - the supporting check passes.
- Reject: The idea is rejected when the main mean is below 0 with t ≤ −2.
- Inconclusive: These results neither confirm nor reject: - a main t between −2 and 2; - a main t ≥ 2 while the supporting check fails. At least 300 independent cases are required, about 17,000 being expected.
