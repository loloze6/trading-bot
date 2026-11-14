---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA above long SMA, from the up cross until the down cross -> adapted: the on/off "above" state is made graded by the SMA spread, kept long only and zero below the cross.
- Comparison: random stretches of the same length -> kept: compared with forward returns from all bars, which is the same as holding the coin.
- Outcome: price rises more often and further until the down cross -> kept: forward returns while the spread is positive, and how the portfolio grows.
- Verdict transfer: yes: the position is open on exactly the bars between the up cross and the down cross, so only its size differs from the idea.
Forecast: The forecast uses one spread, (SMA50 - SMA200) / SMA200, which is the standard 50/200 cross on daily bars. It is standardised against its own past 200 values and clipped at 0. It is positive while SMA50 is above SMA200 and grows with the gap between the two averages. It is zero from the down cross until the next up cross, and it is never negative.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take the coin's forward 20-bar return, sampled every 20 bars so that overlapping returns count once. Compare the mean on bars with forecast > 0 against the mean on all bars, pooled over the 6 windows and judged before costs.
- Supporting check: The share of positive forward 20-bar returns on bars with forecast > 0, compared with the same share on all bars.
- Confirm: The in-situation mean beats the all-bar mean, with a t-stat of at least 2 over the non-overlapping samples. The positive share is also at least 5 points higher. The difference has the same sign in at least 4 of the windows that have in-situation bars.
- Reject: The in-situation mean is at or below the all-bar mean. A t-stat of -2 or lower means reversal or exhaustion, and that also rejects.
- Inconclusive: The idea is neither confirmed nor rejected if the difference is positive with a t-stat between 0 and 2, or if the two measures disagree. The minimum is 15 non-overlapping in-situation samples and at least 2 separate up-cross stretches; with fewer, the result is inconclusive.
