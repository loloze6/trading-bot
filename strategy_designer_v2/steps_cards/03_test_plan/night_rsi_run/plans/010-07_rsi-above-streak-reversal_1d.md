---
idea: 010-07_rsi-above-streak-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: 14-day RSI above 50 without a break, for a number of days up to the close -> kept: RsiMidlineAgeComponent (period 14) counts that unbroken run in daily bars, capped at the default 60.
- Comparison: longer runs against shorter ones ("the longer ... the lower") -> adapted: graded, so the short position grows with the run's length.
- Outcome: lower coin return over the next 14 days -> kept: forward 14-bar return, measured against the coin's mean.
- Verdict transfer: yes: the forecast is the run length itself, so a graded relation between run length and the next 14 days' excess return confirms or rejects the idea directly.
Forecast: The forecast starts from the RSI(14) midline age, which is +n after n unbroken daily closes with RSI above 50, -n below 50, and is capped at 60. It is standardised over the past 160 values. It is then clipped at a minimum of 0, so only the above-50 side is kept, and negated. The forecast is 0 while RSI is at or below 50. While RSI is above 50 it is negative (short), small on the first day of a run and growing more negative the longer the run lasts. It returns to 0 when RSI drops to 50 or below.
Config: 010-07_rsi-above-streak-reversal_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: Use bars on a non-overlapping 14-bar grid per window where the forecast is below 0. On these bars, take the slope of the forward 14-bar return, minus the coin's mean 14-bar return over all windows, against the run length (last_history_value). Pool the three coins and report the slope's t.
- Supporting check: The book's timing gain must be above 0. This is its mean daily return minus the gain from the market's own rise, before costs.
- Confirm: The slope is negative with t ≤ -2 (longer runs, lower excess return), and the timing gain is above 0.
- Reject: The slope is positive with t ≥ +2 (longer runs, higher excess return).
- Inconclusive: Any t between -2 and +2, or a confirming slope whose timing check fails. The test needs at least 100 grid cases with RSI above 50; fewer is inconclusive.
