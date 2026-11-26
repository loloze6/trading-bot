---
line: 7.b inconclusive
backtest: 058-01.g2.b1.g1_three-day-rise-fades-falling_1d
idea tested: 058-01.g2.b1.g1_three-day-rise-fades-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3737 USD
---
## Findings
- **F1:** The test's result is on the predicted side but weak and does not grow with the rise. The mean short-direction unusual 3-day move is +0.70 % (t 1.46, 391 case days, 952 cases; strength 0.075). The slope on |forecast| is -0.0003. In the visible folds B and C the slope of the unusual move on the scaled 3-day rise is -0.00057 a unit (p 0.25), so the larger rises are not given back more, which the brief names as its own test of the theory.
- **F2:** The largest rises do not fade more; they fade least. In folds B and C the case-based unusual move by scaled-rise quartile is +1.21 %, +0.43 %, +1.69 % and -0.10 % over 3 days (t 0.72, 0.43, 1.07, -0.05). Over 5 days it is +3.98 %, +1.39 %, +1.26 % and -3.30 %, and the top quartile (rises of 1.65 to 6.9 usual daily moves) has t -2.03: the coin kept rising after the largest rallies.
- **F3:** The effect changes sign from one period to the next, so the market's own swings in this profile drown it. By year (3-day unusual move): 2018 +0.55 % (t 0.25), 2019 +1.15 % (t 1.12), 2020 -1.38 % (t -1.01), 2021 +2.69 % (t 2.44). By window, w18 shows +3.25 % (t 3.41) while w16 shows -1.31 % (t -0.81) and w17 -2.14 % (t -1.35).
- **F4:** No other horizon gives a clear answer.
- **F5:** There is no one coin where the effect shows clearly; the coins with the most cases show almost nothing. In folds B and C the 3-day unusual move is +0.24 % for BTC (55 cases, t 0.25), -0.29 % for ETH (48, t -0.24) and +0.22 % for XRP (38, t 0.15). Only LINK reaches t 3.10, on 7 cases.
- **F6:** The move barely covers a trade even if it were real. The total move per case is +0.26 % over 3 days against a cost of 0.22 % per trade (1.1 times). Accordingly the book's Sharpe is 0.03, its yearly return is -0.0 % and its Calmar is -0.003.

## Ideas
- No ideas: The test already used every coin and fold available on daily bars. In the visible folds the give-back is neither graded with the rise's size (the largest rises keep rising over 5 days, t -2.03) nor present on any coin, period or horizon with t of 2 or more on a usable number of cases, so the theme's effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
