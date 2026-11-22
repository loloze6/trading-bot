---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's close stands within the range of its closes over the past 20 days, the larger its rise over the next 5 days. This is most pronounced when its 60-day range is narrow rather than wide.
Consequence: A trader leans long on a coin pressing the top of its recent range, and short on one sitting near its bottom, rather than fading those edges.
Why:
- F1: Where the close sits in its own 20-day closing range predicts the next 5 days' excess return. The pooled slope t is between 3.18 and 4.34 across all five 5-day grid offsets (about 3,300 to 3,400 independent cases each), 3.05 to 4.87 at a 3-day horizon and 1.61 to 3.33 at 10 days. It is stronger than the 60-day range position (t 1.90 to 3.19) and stronger than the 30-day return (t 1.70 to 2.90) on every grid.
- F2: Inside a joint regression the 60-day range position keeps its effect (t 2.05), while the 30-day return loses it (t -0.09, 3,419 cases). The idea's monthly-return signal adds nothing once nearness to the top of the range is known.
- F3: The 60-day range-position effect is a continuation, not the reversion the brief expects. The top quintile is +1.49 % in excess over 5 days (t 2.37, 341 cases) and the second quintile -1.40 % (t -3.08). At 10 days the top quintile is +2.56 % (t 2.33, 168 cases). The effect shows in the narrow and middle terciles of 60-day range width (slope t 2.71 and 3.44) and vanishes in the widest tercile (t -0.51).
- F4: The range-position effect is not stable over time. Its pooled slope t is 4.67 in 2018–2021 and -1.98 in 2022–2025. Per coin it is positive everywhere but significant only for XRP (t 2.28), with ETH at t 1.93 and BTC, LTC, XMR and ZEC between 0.15 and 1.02.
