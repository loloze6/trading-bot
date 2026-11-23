---
line: 7.b inconclusive
backtest: 031-01_near-yearly-low-keeps-falling_1d
idea tested: 031-01_near-yearly-low-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3429 USD
---
## Findings
- **F1:** The result points the way the idea predicts but falls short of the bar. The 20-day slope of the drift-adjusted short gain on |forecast| is 0.00236 (t 1.70, 806 cases). All of it sits in the top fifth of |forecast|, which gains +4.88 % per case (t 1.82 with same-day cases taken together, 162 cases on 69 days). The other four fifths gain -0.00 %, -1.05 %, +0.10 % and -3.93 %, so the effect is not graded below the top fifth.
- **F2:** The slope comes from the market's bad years, not from closeness to the low within a year. Once each year's mean short gain is removed, the 20-day slope is -0.00062 (t -0.46, 806 cases), and it is near 0 at 5 days (t -0.11) and 10 days (t 0.36). The top-fifth cases fall mostly in 2018 (56 cases, +11.2 %) and 2022 (48 cases, +5.9 %). Each other year has only 8 to 12 such cases, mostly negative, for example 2020 at -15.6 % and 2024 at -6.3 %.
- **F3:** The raw closeness to the yearly low does not predict the move. The 20-day slope on raw proximity has t 1.08, and on log-proximity t 0.03. The median case sits about 78 % above its yearly low, and only 23 of 806 cases are within 1.5 % of it. Within 0.05 % of the low, the 17 cases at 20 days gain +9.2 %, but the 25 cases at 10 days gain -3.8 %.
- **F4:** Across horizons the pooled slope is positive at 5 days (t 2.07, 3,326 cases) and at 10 days (t 2.43, 1,646 cases). It weakens to t 1.70 at 20 days and to t 0.53 at 40 days (386 cases), so the plan's 20-day horizon is not where the pooled slope is strongest. These pooled slopes still carry the year effect of F2.
- **F5:** The direction holds across coins. The top fifth's 20-day short gain is positive on all six coins, from +2.9 % (XMR) to +7.6 % (ETH), with 24 to 31 cases each. The slope is positive on five coins (t 0.29 to 1.68) and zero on ZEC (t -0.02), so no single coin carries the result.
- **F6:** The book cannot pay as tested. The idea's size is an unusual move of -1.41 % per case (t -0.75, 394 cases on 243 days), and the total move is -4.44 %, because the short runs against the coins' rising drift. One trade costs 0.19 %. The book's Sharpe is -0.30, its yearly return -16.4 %, and it holds a position on 86 % of the coins' days.

## Ideas
- `031-01.b1_near-yearly-low-falls-all-coins` (from F1, F5): The closer a coin's daily close is to its lowest close of the past 365 days, the more it falls over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
