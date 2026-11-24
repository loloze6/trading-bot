---
idea: 031-04_down-streak-length-continuation
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a coin has closed lower several days in a row -> replaced: no component outputs the count of consecutive down closes; the nearest, `DownStreakLossInUsualMovesComponent`, measures the streak's summed loss, not its length.
- Comparison: the streak's length against the coin's own down-close streak lengths over the past 365 days -> replaced: `standardise` over 365 bars would scale by the mean daily reading, not by the lengths of past completed streaks.
- Outcome: it keeps falling over the next 5 days, more so the longer the streak -> kept: a short position graded by relative streak length, held 5 bars.
- Verdict transfer: no: a test on streak loss size, or on a day-weighted scale, could confirm or reject a different quantity than streak length against past streak lengths.
Reason: The idea needs the length of the current run of lower closes, ranked against the lengths of the coin's down-close streaks completed over the past 365 days. Both come from the coin's own closes and the config could hold them, but no catalogue component outputs the streak count or that rank. `DownStreakLossInUsualMovesComponent` (summed loss), `DownStreakVolumeFadeComponent` (volume slope), `RsiMidlineAgeComponent` and `MovingAverageAgeComponent` (other sides) cannot give them, alone or in combination.
