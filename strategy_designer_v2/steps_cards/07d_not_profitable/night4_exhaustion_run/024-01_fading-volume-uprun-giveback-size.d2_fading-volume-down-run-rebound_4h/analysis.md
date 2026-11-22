---
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3464 USD
---
## Findings
- **F1:** The book's deepest fall was -57.1 % over 83 days across w16–w17, deeper than holding the coins over the same days (-43.9 %). The book's daily returns move with holding's (correlation 0.86), and on its worst 5 % of days the book lost -6.6 % while the coins lost -8.5 %. Its falls are the market's falls, which gives the failing Calmar of 0.33.
- **F2:** The idea adds no move of its own. Its unusual 18-bar move is +0.00 % per case (t 0.002, 4537 cases), and the total move (+0.41 %) is only the coins' normal drift. The book holds a position on 78 % of bars at a mean allocation of about 0.68, so it is mostly a part-time long on the coins.
- **F3:** Bars held after a low 30-day return pay nothing but carry full risk. The book's mean bar gain in the lowest 30-day-return quintile is +0.000009 (t 0.06, n 12279, sd 0.0160) and in the second -0.00020 (t -1.56). In the highest quintile it is +0.00065 (t 4.08, n 12400), and the 7-day return shows the same pattern (lowest quintile +0.00014, t 0.88; highest +0.00062, t 4.07).
- **F4:** The rebound shows only after a strong prior week. Cases in the highest 7-day-return quintile have an unusual 18-bar move of +1.63 % (t 1.58, n 102) and the second-lowest -0.89 % (t -1.34, n 124). By 30-day return, the highest quintile is +1.60 % (t 1.19, n 75) and the middle ones are about -0.27 %.
- **F5:** The rebound concentrates where 7-day volatility is high against 30-day volatility. In the top quintile of that ratio, cases rise +2.30 % above drift over 18 bars (t 1.98, n 102), against -0.43 % to +0.65 % in the other four quintiles. The book's bar gain there is +0.00097 (t 4.88), against -0.00003 to +0.00012 elsewhere.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.d1_fading-dip-in-rising-week` (from F1, F3, F4): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise, only while the coin's 7-day return is positive, the rise growing the higher that 7-day return.
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.d2_fading-dip-under-volatility-burst` (from F2, F5): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise, the rise being larger the more the coin's 7-day volatility exceeds its 30-day volatility.
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.d3_monthly-return-carries-forward` (from F3): The higher a coin's 30-day return, the more it rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
