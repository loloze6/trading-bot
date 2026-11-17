---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3130 USD
---
## Findings
- **F1:** The verdict's check fails because the down-minus-up gap is concentrated in large moves. On active bars with |vol-scaled move| ≥ 1, down days reverse more than up days by 0.0121 (Welch t 4.03; 722 down, 846 up). On smaller moves the gap is −0.0010 (t −0.74; 3200 down, 3303 up). Pooled, this gives the verdict's 0.0015 at Welch t 1.23.
- **F2:** The grading in the idea holds only on the down side. Regressing next-day reversal on |vol-scaled move| gives a slope of 0.0068 (t 4.17, n 3266) after down days, but −0.0016 (t −1.26, n 3469) after up days. In the active regime the reversal is 0.0106 (t 3.54) for falls of 1 to 1.5 vols and 0.0215 (t 2.89) for falls beyond 2 vols. For up moves beyond 1.5 vols it is −0.0065 (t −1.61) and 0.0026 (t 0.58).
- **F3:** The book's gain also comes from the long side. Gain per bar is 0.00204 (t 5.18, n 3902) when long after a fall, against 0.00051 (t 1.34, n 4152) when short after a rise.
- **F4:** The large-move down-minus-up gap is positive in all 8 years, from 0.0058 to 0.0259 (Welch t 0.70 to 2.64). Year-by-year it is mixed only when all moves are included, from −0.0040 to 0.0044.
- **F5:** The regime matters. Outside the high-volatility regime, next-day reversal is −0.0009 (t −1.43) after down days and 0.0005 (t 0.75) after up days. Inside it, these are 0.0043 (t 4.75) and 0.0028 (t 3.43).
- **F6:** The pooled down-minus-up gap is on the side the idea predicts, at 0.0015 (Welch t 1.23 on 3922 vs 4149 bars). It would need roughly 2.6 times as many cases to reach t 2 at the same size, and the backtest used only 6 of the 19 coins available.

## Ideas
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.b1_high-vol-down-day-rebound` (from F1, F2, F3, F4, F5): When a coin's 20-day volatility is high relative to its own 120-day volatility, its last day's fall reverses over the next 1 day: the larger that day's fall measured in its 20-day volatility, the larger the rise back.
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.b2_vol-regime-reversal-more-coins` (from F6, F1): When a coin's 20-day volatility is high relative to its own 120-day volatility, its last day's move reverses over the next 1 day. The larger that day's return measured in its 20-day volatility, the larger the move back, and the reversal is stronger after down days than after up days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
