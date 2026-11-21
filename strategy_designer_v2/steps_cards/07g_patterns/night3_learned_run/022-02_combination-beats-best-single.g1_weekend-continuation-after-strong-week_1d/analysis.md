---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
idea tested: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3703 USD
---
## Findings
- **F1:** The tested idea's own edge is the strongest pattern in the bars. Measured from Friday's close, the correlation between a coin's 7-day return (scaled by its 20-day volatility) and Saturday's volatility-scaled excess return is 0.146 (t 6.7, 2070 days, 6 coins). On the other six weekdays it runs from -0.058 to +0.071. By quintile of the 7-day return, Saturday's excess return climbs evenly from -0.45 % to -0.12 %, +0.15 %, +0.52 % and +1.14 %.
- **F2:** The Saturday continuation grows with volatility. By quintile of the coin's own 20-day volatility, the correlation is 0.12 (t 2.4) and 0.14 (t 2.9) in the two calmest fifths, against 0.20 (t 4.3) and 0.25 (t 5.4) in the two most volatile, with 388 to 426 days each.
- **F3:** Longer trends and nearness to highs also carry into Saturday, and almost only Saturday. From Friday's close, the scaled 28-day return correlates with Saturday's excess return at 0.099 (t 4.3, 1908 days), against at most 0.040 (t 1.7) on other days. Distance below the 28-day high correlates at 0.089 (t 3.9), against at most 0.044 (t 1.9) on other days.
- **F4:** Part of the weekend move reverses on Sunday. From Saturday's close, the scaled one-day return correlates with Sunday's excess return at -0.081 (t -3.7, 2069 days). The 7-day return also turns slightly against Sunday: -0.058 (t -2.65). Holding from Friday's close for two days, the 7-day correlation drops from 0.146 to 0.088 (t 4.0, 2046 days).
- **F5:** On any day, a large fall is followed by a rebound. Across deciles of the volatility-scaled one-day return (about 1450 days each), the lowest decile's next-day excess return is +0.53 % (t 3.6) and the second lowest is +0.25 % (t 2.0). From the middle deciles up, it is -0.04 % to -0.22 % with |t| < 2, and the top decile shows nothing (+0.03 %, t 0.2). The rebound is one-sided: falls rebound, rises do not reverse.
- **F6:** The 7-day trend also continues into Monday. From Sunday's close, the scaled 7-day return correlates with Monday's excess return at 0.071 (t 3.2, 2069 days). This is the only other weekday above t 3.
- **F7:** The book earns on one day in seven, which explains why it fails on mean daily return.
- **F8:** The Saturday edge is uneven across windows and coins.
- **F9:** The volatility level alone predicts nothing for the next day. Next-day excess return by volatility quintile runs from -0.10 % to +0.15 %, with |t| ≤ 1.4.

## Ideas
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.g1_volatile-week-weekend-continuation` (from F1, F2): On a Saturday, a coin's return over the next day rises more steeply with its 7-day return the higher the coin's volatility over the past 20 days.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.g2_monthly-trend-into-saturday` (from F3, F1): On a Saturday, a coin's return over the next day is larger the higher its return over the preceding 28 days.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.g3_sunday-reversal-of-saturday` (from F4): On a Sunday, a coin's return over the next day is lower the higher its return over the preceding day.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.g4_rebound-after-sharp-daily-fall` (from F5, F9): On any day, a coin's return over the next day is larger the deeper its fall over the preceding day, measured against its volatility over the past 20 days.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.g5_weekly-trend-into-monday` (from F6, F7): On a Monday, a coin's return over the next day is larger the higher its return over the preceding 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
