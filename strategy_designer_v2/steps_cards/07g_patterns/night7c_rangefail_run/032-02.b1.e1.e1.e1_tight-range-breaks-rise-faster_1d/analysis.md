---
line: 7.g patterns
backtest: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster_1d
idea tested: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3677 USD
---
## Findings
- **F1:** Across all bars on the 5-day non-overlapping grid, the higher the close sits in its prior 60-day range of closes, the larger the unusual 5-day move that follows. The top fifth (mean place 0.96) is followed by +2.88 % (t 3.13, 169 cases) and the bottom fifth by −1.66 % (t −1.50), with strengths of +0.23 and −0.13 of a usual move. The pooled Spearman is 0.156 (p 5e-6), and the day-clustered t is 2.14 over 152 days.
- **F2:** The F1 ordering points the same way on all 6 coins (Spearman 0.11 to 0.23) and in 3 of 4 years, but it is positive in only 5 of 12 windows. Much of it may therefore come from differences between windows rather than from within one window.
- **F3:** The F1 ordering is stronger when the coin is calm: Spearman 0.215 in the lower half of 20-day volatility (426 cases) against 0.064 in the upper half (420 cases).
- **F4:** The same ordering holds over 10 days and over a 20-day range. Over 10 days the top fifth of the 60-day place gains +5.10 % (t 2.83, 83 cases) against −1.08 % for the bottom fifth. For the 20-day range place, the top fifth gains +2.34 % (t 3.08, 285 cases) and the bottom fifth −2.13 % (t −2.71).
- **F5:** On closes above the prior 60-day closing high (44 grid cases), the calmest third by 20-day volatility (mean 2.8 %) gains +11.2 % unusual over 5 days (t 5.61, 15 cases), the middle third +6.1 % (12 cases) and the most volatile third +2.0 % (t 0.66, 17 cases). The small breaks (mean 1.1 % past the high) gain +7.7 % (t 3.28), against +1.0 % for the largest breaks (8.3 %).
- **F6:** Closes below the prior 60-day closing low do not come back: their mean unusual 5-day move is +0.01 % (t 0.00, 58 cases). Neither side shows the failed break the brief expects.
- **F7:** The book is in a position on 59 % of top-fifth range-place bars and on under 10 % of the others, so its profit sits on the bars where F1's ordering is strongest.

## Ideas
- `032-02.b1.e1.e1.e1.g1_place-in-range-predicts-drift` (from F1, F2, F3, F4, F7): The higher a coin's daily close sits within its range of closes over the prior 60 days, the larger its rise over the next 5 days, and the more so the calmer its daily returns over the prior 20 days.
- `032-02.b1.e1.e1.e1.g2_calm-breakouts-rise-further` (from F5, F3): When a coin closes above its highest close of the prior 60 days, the lower the standard deviation of its daily returns over the prior 20 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
