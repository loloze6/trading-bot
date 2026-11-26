---
line: 7.e profitable but not proven
backtest: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d
idea tested: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4221 USD
---
## Findings
- **F1:** Breakouts in general carry the book, not the run-up discount. In folds B and C, the first close above the prior 60-day high in each 20-day grid cell is followed by a mean 20-day excess return of +14.4 % (47 cases, 34 days, t 3.63), and +10.6 % over 10 days (84 cases, t 2.73). Grid cells without a breakout are followed by −9.2 % over 20 days (141 cases, t −2.42).
- **F2:** The tested grading is absent. On breakout cases, the 20-day excess return has no slope on the prior 60-day return (t −0.22, Spearman 0.02, 46 cases). Its run-up terciles show no order: low 13.4 %, mid 19.0 %, high 9.8 %.
- **F3:** The narrowness of the prior range does grade the follow-through. Breakouts out of the tightest third of 60-day high-to-low close ranges gain +23.5 % excess over 20 days (16 cases, t 3.37), against +11.8 % for the middle third (t 1.63) and +7.6 % for the widest third (t 1.23). The slope on range width is negative over 20 days (t −2.07) and over 10 days (t −2.15, 84 cases).
- **F4:** A smaller overshoot is followed by a larger continuation, not a larger giveback. Breakouts closing least past the prior 60-day high gain +21.1 % excess over 20 days (16 cases, t 2.49), against +7.3 % for the largest overshoots (t 1.26). Over 40 days the slope on overshoot is −4.17 (t −3.85, 23 cases), with small overshoots at +29.3 % and big ones at +7.1 %.
- **F5:** The book's gain is timing more than drift but leans on one year. Its mean daily return of 0.076 % splits into 0.017 % from the market's rise and 0.059 % from timing (Sharpe 1.36 against 0.53 for holding, 1449 days). Of its trades' 1325 summed net percent, 1194 came from trades entered in 2020, and the top 10 of 112 trades made 762. Breakouts in 2020 gain +23.7 % excess over 20 days (t 3.76), against +5.3 % in 2021 (t 0.85).
- **F6:** The breakout follow-through is uneven across coins. Over 20 days it is +22.4 % for XMR (t 5.28) and +37.0 % for XRP (t 2.10), but only +2.1 % for BTC (t 0.39). LTC added only 0.012 to the book's summed return.

## Ideas
- `032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further` (from F1, F3, F5): When a coin closes above its highest close of the prior 60 days, the narrower its 60-day range between highest and lowest close, the larger its rise over the next 20 days.
- `032-02.b1.e1.e1.e1.e2.e2_small-overshoots-keep-climbing` (from F1, F4): When a coin closes above its highest close of the prior 60 days, the smaller the distance by which that close exceeds the prior high, the larger its rise over the next 40 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
