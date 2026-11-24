---
line: 7.g patterns
backtest: 031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound_1d
idea tested: 031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7314 USD
---
## Findings
- **F1:** Within each coin, the 14 days after the bars where the 10-day volatility stood lowest against the 60-day volatility (bottom fifth, log ratio -0.73) ended -7.2 % below the coin's mean 14-day return (t -3.25 over 41 days, 154 cases). The other fifths ranged from +0.6 % to +3.4 %. The slope on the ratio's rank was +0.53 (day-clustered t 2.26, 732 cases, 79 days) and positive in 16 of 16 coins. It held with the 30-day volatility level in the regression (t 2.32). It is a recent-years effect (2022–2025: t 3.04; 2018–2021: t 0.03). It is horizon-specific: t 0.98 at 7 days, -0.29 at 21 days, 1.10 at 30 days. With the many angles looked at, it is suggestive rather than settled.
- **F2:** A coin's 30-day volatility against its own average leaned against the next move. The 14-day slope on its rank was -0.43 (t -2.09, 131 days) and negative in 16 of 17 coins. Over 30 days, the calmest within-coin third rose +11.5 % against +1.0 % and -0.8 % for the other two thirds (excess +0.23 usual move, t 1.39, 39 days; rank correlation -0.16 over 676 cases). The day-clustered 30-day slope is only t -1.53.
- **F3:** At 30 days the bars show continuation, not reversal. Price near its 60-day high predicted a higher 30-day excess return (slope +0.40, t 1.95, positive in 14 of 15 coins). The top fifth of the 30-day move, scaled to the coin's usual, was followed by +5.1 % excess (t 1.33). The bottom fifth was followed by -6.2 % (t -1.31), with 13 of 15 coins leaning the same way. This is against the brief's overreaction story, though no single cut reaches t 2.
- **F4:** The tested book's gain is not graded by its forecast. Net trade P/L by entry-forecast quartile was +4.9 %, +8.7 %, +4.9 % and +6.3 %, with the top quartile saturated at 20. The tested idea's unusual move is +3.84 % per case with t 1.10 over 99 days. Its trades lost in 2019 (-2.7 %, 45 trades) and 2022 (-1.2 %, 83 trades) and won in 2023–2024 (+13.6 %, +12.3 %). XRP's 35 trades averaged +30.8 %, against -5.4 % for BTC.
- **F5:** The weekday pattern is not real. Once days are taken together across coins, no weekday stands out: the largest |t| is 2.10 (Saturday) among 7 weekdays, and Saturday's mean falls from +0.106 to +0.029 standard deviations between the early and late halves.

## Ideas
- `031-02.b2.a1.b1.g1_volatility-compression-precedes-weakness` (from F1): The further a coin's volatility over the past 10 days has fallen below its volatility over the past 60 days, the more its price falls below its usual drift over the next 14 days.
- `031-02.b2.a1.b1.g2_calm-coins-outperform-next-month` (from F2, F1): The lower a coin's volatility over the past 30 days stands against its own usual volatility, the more its price rises above its usual drift over the next 30 days.
- `031-02.b2.a1.b1.g3_near-high-continuation-over-month` (from F3, F4): The closer a coin's price stands to its highest close of the past 60 days, the more it rises above its usual drift over the next 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
