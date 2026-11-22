---
idea: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars with a large loss in typical 4h moves -> adapted: "large" becomes a graded size, the streak's loss divided by the mean absolute 4h move, and "after the streak" becomes "while the streak runs".
- Comparison: the coin's typical 4h move over the past 30 days -> kept: the mean absolute one-bar return over 180 bars.
- Outcome: the coin rises over the next three days, more after deeper streaks -> kept: a long position sized by streak depth, held 18 bars.
- Verdict transfer: yes: the forecast is the streak's loss in usual moves, long only, held for the idea's three days.
Forecast: The forecast uses DownStreakLossInUsualMovesComponent with window 180, which is 30 days of 4h bars, side "down" and base "start". - Raw value: the loss of the current unbroken run of down-closing bars, as a share of the price where the run started, divided by the coin's mean absolute 4h return over the last 180 bars. It is 0 on any bar that did not close down. It is never negative. - Scale: standardise puts the value on its own past scale, using a 180-bar window with 45 minimum periods. - Dead zone: signed_power with exponent 3 and pivot 10 damps short or shallow streaks towards 0 and amplifies deep ones. This is the strongest graded dead zone allowed, because a deep streak is a rare extreme. - Sign and size: the forecast is positive (long) while a falling streak runs, and grows steeply with the streak's depth in usual moves. It is zero on bars that did not close down, and it is never short. - Gating: there is no regime gate.
Config: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a long bet (a forecast rise of at least 2 points), read once per cell of the non-overlapping 18-bar grid in each window. The measure is the case's unusual move: the coin's 18-bar return from the signal bar's close, minus the coin's mean 18-bar return over all its windows. It is pooled over coins as a mean with its t.
- Supporting check: Split the cases at the median forecast at the signal bar. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move has t ≥ 2 over at least 30 independent cases, and the supporting check passes (upper half minus lower half > 0).
- Reject: The mean unusual move has t ≤ -2 over at least 30 independent cases.
- Inconclusive: The result is inconclusive in any of these cases: - t is between -2 and 2; - t ≥ 2 but the upper-half minus lower-half difference is not above 0; - there are fewer than 30 independent cases.
