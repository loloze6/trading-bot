---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5149 USD
---
## Findings
- **F1:** Sunday is the only day whose move clearly reverses over the next 3 days. The correlation of the Sunday bar's vol-scaled return with the next 3 days' excess over drift is -0.094 (p < 0.0001, n = 4320). Every other weekday lies between -0.021 and +0.051.
- **F2:** The Sunday reversal works on both sides of the move. Sunday rises are followed by -1.02 % against drift over 3 days (t -5.48). Sunday falls are followed by +0.97 % (t +4.67).
- **F3:** Across Sunday quintiles of the scaled return, the next 3 days' excess falls from +1.37 % (t 3.86) through +1.11 %, -0.54 % and -1.17 % to -0.97 % (t -3.05) at the top. The effect is graded across the whole range but flattens among the largest rises, which matches the tested short-only plan's weighted correlation of -0.001.
- **F4:** The Fri-to-Sun two-day weekend move, scaled the same way, predicts nothing. Its quintiles give +0.43 %, -0.07 %, -0.56 %, -0.14 % and +0.13 %, all with |t| ≤ 2.1. The reversal belongs to Sunday's own bar.
- **F5:** Sunday rises reverse most in coins that were already falling. After a 20-day decline (mean -17.5 %) the 3-day excess is -1.58 % (t -5.62). It is -0.72 % (t -2.80) in the flat tercile and -0.75 % (t -1.84) after a 20-day rise of +36 %.
- **F6:** Low weekend volume does not grade the reversal, contrary to the brief. Sunday-rise terciles of weekend volume against the 20-day mean give -1.44 % (t -5.26), -0.45 % (t -1.41) and -1.16 % (t -3.16).
- **F7:** The Sunday-rise shortfall is spread over most coins and years. It is negative in 17 of 19 coins and in 7 of 8 years, strongest in 2018 (-3.69 %, t -4.10) and 2024 (-1.74 %, t -3.82), and weak in 2020–2023 (|t| ≤ 1.2).
- **F8:** Weekday moves do not reverse, in contrast to Sunday. Wednesday rises of more than one vol continue over the next 3 days (+1.52 %, t 4.10, n = 765), and so do Thursday rises (+1.03 %, t 2.49).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week.g1_sunday-move-reverses-both-ways` (from F1, F2, F3, F4): A coin's Sunday close-to-close return, measured against its 20-day volatility of daily returns, is followed by a move the other way over the next 3 days. After a Sunday fall the coin beats its normal drift, after a Sunday rise it falls behind, and the larger the Sunday move, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week.g2_sunday-bounce-in-downtrend-fades` (from F5, F2, F7): A coin that rose on Sunday, measured against its 20-day volatility, falls behind its normal drift over the next 3 days by more the further it fell over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
