---
line: 7.g patterns
backtest: 031-02.b1.g2.b1_volatile-falls-more-coins_1d
idea tested: 031-02.b1.g2.b1_volatile-falls-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5935 USD
---
## Findings
- **F1:** The book is mostly a scaled long position in the coins, not a fall-rebound timing book: its daily returns correlate with holding the coins at 0.77 to 0.86 in every year from 2018 to 2025. The mean position is 0.43 of the book. On the book's best 5 % of days it earns 543 bp while the coins rise 799 bp, and on its worst 5 % it loses 566 bp while the coins fall 858 bp, about 0.65 of the coins' move both ways.
- **F2:** The latest day's return does not grade the next 2 days monotonically. On each coin's own deciles of the 1-day return, the mean excess 2-day return runs +0.51 % (t 0.85), +0.28 %, +0.01 %, -0.38 % (t -1.55), -0.08 %, -0.12 %, -0.07 %, -0.42 % (t -1.88), -0.37 %, +0.36 % (t 1.02). The regression of the excess 2-day return on the volatility-scaled day return has slope t -0.03 (9087 cases, 765 days).
- **F3:** Streak length does not grade the following move in either direction. For down streaks of 1 to 5+ days, the excess 2-day return is -0.19 %, +0.10 %, +1.01 %, +0.13 %, +0.36 %, every one with |t| ≤ 1.37. For up streaks it is -0.29 %, -0.08 %, +0.30 %, -0.32 %, +0.63 %, every one with |t| ≤ 1.53. Over 5 days the signs flip between neighbouring lengths, for example -2.79 % (t -1.84) after 4 down days against +1.28 % (t 1.55) after 3.
- **F4:** The past 20-day return scaled by 60-day volatility leans towards continuation over the next 10 days, but not reliably. The slope is +1.66 % per unit with t 2.08 (1739 cases, 151 days). Over the ten possible grid offsets t ranges from 0.45 to 2.49, mostly between 0.7 and 1.5. The yearly slopes change sign (2022: t -2.47; 2019: t +2.38). It is positive on 15 of 18 coins, but only one coin reaches |t| ≥ 2 (XRP 2.06). At 2, 5, 7, 14 and 20 days the same measure has t 1.80, 1.34, 0.91, 0.40 and 1.20.
- **F5:** The 20-day-return quintiles give a U shape at 2 days, not a graded effect. The excess return runs +0.36 % (t 0.87), -0.61 % (t -2.49), -0.17 %, -0.11 %, +0.58 % (t 1.96). The 5-day and 10-day quintiles have a similar shape, with the second quintile at -0.84 % and -3.16 %. None of these exceeds a |t| of 2.5, out of roughly 70 cells examined.
- **F6:** Calendar and volatility splits show nothing. By weekday, the excess 1-day return has |t| ≤ 1.73 on every weekday. By 60-day volatility tercile, the excess 2-day return is +0.13 %, -0.29 % and +0.16 % (|t| ≤ 1.12). The only |t| of 3 in all the tables, -1.90 % over 5 days in the third 1-day-return decile, is isolated between neighbours of +0.0 % and -0.95 %.

## Ideas
- No ideas: Across about seventy cells of forecast, streak, past-return, volatility, weekday, year and book-tail splits, no pattern stands out from chance once that many looks are counted. The best candidate, 20-day continuation over 10 days (F4), drops to a |t| of about 1 on most grid offsets and flips sign between years. The book's profit is the coins' own rise held at about 0.43 (F1), which leaves no new effect to propose.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
