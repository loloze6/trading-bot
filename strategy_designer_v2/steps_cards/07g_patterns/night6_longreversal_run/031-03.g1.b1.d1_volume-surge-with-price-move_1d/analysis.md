---
line: 7.g patterns
backtest: 031-03.g1.b1.d1_volume-surge-with-price-move_1d
idea tested: 031-03.g1.b1.d1_volume-surge-with-price-move
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4518 USD
---
## Findings
- **F1:** Volume alone predicts the next 14 days whatever the coin's 14-day price move did. Taking each case in the direction of the sign of the 14-day over 30-day volume ratio gives an unusual move of +2.96 % per case, t 3.15 with the cases of one day taken together (1530 cases, 131 days), strength 0.135 of the coin's usual move. That is 13 times the 0.22 % cost of a trade, against +1.13 % (t 1.70) for the tested idea, which gated the volume signal by price.
- **F2:** The two cases the tested idea stood aside in carry the strongest moves. When the 14-day return is up but volume is below its 30-day mean, the next 14 days are -3.89 % unusual (t -3.93, 331 cases). When the 14-day return is down but volume is above its 30-day mean, they are +2.03 % (t 2.05, 316 cases).
- **F3:** The volume effect is graded, and its low end looks the same whichever way price moved.
- **F4:** The larger volume excesses carry the move. In the half of cases with the larger standardised volume ratio in absolute value, the volume-sign bet earns +4.60 % (t 3.58, 122 days); in the smaller half it earns +1.32 % (t 1.26, 119 days).
- **F5:** The volume-sign bet is positive in 6 of 8 years and largest in the latest ones: 2023 +4.3 % (t 1.99), 2024 +6.6 % (t 2.33), 2025 +2.8 % (t 1.82). It is slightly negative in 2018, 2019 and 2022.
- **F6:** The volume signal fades with a shorter window on either side.
- **F7:** The book's gain came from its long side, and its short side lost.
- **F8:** Other angles were checked and none stands out once the cases of one day are taken together and the many angles looked at are counted.

## Ideas
- `031-03.g1.b1.d1.g1_volume-swell-leads-price` (from F1, F2, F3, F4, F5, F6): The more a coin's mean daily volume over the last 14 days has risen above its mean daily volume over the last 30 days, the more its price rises over the next 14 days. The more that volume has fallen below its 30-day mean, the more its price falls over the next 14 days, whichever way its price moved over those 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
