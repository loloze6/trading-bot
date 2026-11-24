---
line: 7.g patterns
backtest: 031-03.b1.a1_yearly-low-break-all-coins_1d
idea tested: 031-03.b1.a1_yearly-low-break-all-coins
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4161 USD
---
## Findings
- **F1:** The tested situation is too rare to judge. Closes below the prior 365-day closing low fill 1.5 % of the coin-day rows. On the 10-day grid they give 47 cells with a mean unusual move of +2.1 % (t 1.07, against −0.03 % and t −0.11 on the other 3,002 cells), and the verdict counted only 18 cases on 16 days. The measured size, +6.84 % or 0.42 of a usual move, rests on too few days to tell from chance.
- **F2:** Past momentum may carry into the next 10 days, but not clearly enough to count. The coin's own past-return rank against its next 10-day unusual move has a day-clustered slope t of 1.77 for the 10-day return (2,790 cases, 280 days), 1.84 for the 30-day return (2,272 cases, 229 days) and 1.76 for the vol-scaled 30-day return. The top quintile sits near +2.4 % and the second-lowest near −2.4 %, with the lowest quintile back near 0, so the effect is not a clean grade either.
- **F3:** Very large one-day falls may be followed by a short rebound, but it does not hold up. After a daily drop beyond 3 times the coin's 60-day volatility, the next 3 days run +3.0 % above the coin's mean (t 2.30, 170 cases on 60 days). The next day (+1.6 %, t 1.02) and the next 5 days (−0.5 %, t −0.32) are not distinguishable from zero. Within falls beyond 2 times, the depth of the fall does not grade the rebound (Spearman 0.015, p 0.70, 618 cases).
- **F4:** The Thursday-start 10-day cells look strong at first (+3.6 %, naive t 4.37), but taking the cases of one day together cuts this to t 1.83 on only 43 days.
- **F5:** Calendar years differ widely: the 10-day unusual move runs from −4.5 % (t −3.0) in 2018 to +2.7 % (t 2.6) in 2020. These are market-wide swings, not a pattern in one coin's own bars.
- **F6:** The bars show nothing by volatility level: the 20-day volatility quintiles range from −0.7 % to +0.4 % with every t under 1.2 (Spearman p 0.10).

## Ideas
- No ideas: Across about 40 cells (past returns, 30-day lows and drawdowns, volatility, weekday, year, one-day shocks over 1, 3 and 5 days, and the yearly-low regime itself), only one result beats t 2 once the cases of a day are taken together: the 3-day rebound after a 3-sigma fall at t 2.30. That result is contradicted by its own 1-day and 5-day readings and by the missing grade. Given how many angles were tried, nothing stands out enough to support a new idea, and the tested idea itself needs more cases than these coins and folds contain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
