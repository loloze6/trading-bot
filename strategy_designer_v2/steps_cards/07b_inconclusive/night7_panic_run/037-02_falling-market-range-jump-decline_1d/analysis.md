---
line: 7.b inconclusive
backtest: 037-02_falling-market-range-jump-decline_1d
idea tested: 037-02_falling-market-range-jump-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3220 USD
---
## Findings
- **F1:** The tested measure falls on the side opposite the idea and cannot be told from zero at any horizon. On folds B and C, the unusual move in the short direction after wide days in falling markets averages -0.12 % over 3 days (t -0.15, 284 cases), -0.34 % over 1 day (t -0.53), +0.57 % over 5 days (t 0.53) and +0.01 % over 10 days (t 0.01).
- **F2:** The effect is not graded by the width of the day. The correlation of the range multiple with the 3-day short-side excess move is 0.024. By range-multiple quartile the mean is -1.22 % (t -1.07), -0.33 % (t -0.25), +1.40 % (t 1.25) and -0.34 % (t -0.16) from narrowest to widest.
- **F3:** The result flips sign over time rather than living in one part of the data. The 2018 cases average +1.81 % (t 1.40, 125 cases) and 2019 cases +0.58 % (t 0.41). The 2020 cases average -3.37 % (t -1.63) and 2021 cases -4.54 % (t -1.85), with window w18 at -6.62 % (t -2.35, 19 cases), a rebound against the short.
- **F4:** No market sub-condition carries the effect.
- **F5:** By coin the 3-day short-side mean ranges from -1.66 % (XMR, t -1.32) to +0.97 % (ETH, t 0.70). No coin reaches |t| 2.
- **F6:** The idea cannot pay. Its unusual move per case (-0.22 %, strength -0.025) is -1.1 times the 0.19 % cost of a trade. The book's Sharpe is -0.28 and its yearly return is -6.0 %.

## Ideas
- No ideas: The theme's effect is not in the data. Wide days in falling markets are followed by no decline at any horizon from 1 to 10 days (F1), with no gradient in the day's width (F2) and no coin, close direction, fall depth or prior-move condition that carries it (F4, F5). The only split that separates is by period, and there the later years rebound against the short (F3).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
