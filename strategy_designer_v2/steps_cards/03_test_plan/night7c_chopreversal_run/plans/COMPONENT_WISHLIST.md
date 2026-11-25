# Component wish list

One block per idea that needs components the catalogue does not have.

## 032-03_reversal-grows-with-choppiness_1d
- Component: ChopWeightedScaledReversal: -(close[t]/close[t-7] - 1) / (std, ddof 1, of the last 30 daily close returns x sqrt(7)) x (1 - ER30), where ER30 = abs(close[t] - close[t-30]) / sum of abs daily close changes over those 30 bars; closes only; signed against the 7-day move, its size grows with the move in usual swings and as the 30 days get choppier (0 for a straight-line trend) | measures: situation
