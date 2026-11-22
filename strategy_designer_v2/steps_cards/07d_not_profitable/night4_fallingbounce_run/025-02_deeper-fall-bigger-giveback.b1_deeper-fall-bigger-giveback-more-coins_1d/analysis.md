---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
idea tested: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6430 USD
---
## Findings
- **F1:** The coin gives back part of the bounce on the next day only. On the 466 bounce bars in the regime, the coin's next-day return beat its normal daily drift by -0.58 % (t -2.28). Over days 2 to 5 it beat its drift by +0.20 % (t 0.36), and the plan's 5-day measure shows an unusual move of -0.10 % per case (strength -0.005, 376 cases).
- **F2:** The next-day giveback grows with the size of the bounce. Regressing the next-day return in usual daily moves on the bounce size gives a slope of -0.116 (t -2.55, 377 cases). The giveback is -0.71 % after a bounce of 2 to 2.5 usual moves, -1.16 % after 3 to 4 (t -1.96) and -2.33 % after more than 4 (t -2.35, 50 cases).
- **F3:** The depth of the 90-day fall, which the forecast is sized by, does not grade the 5-day move. The plan's slope t is -0.47. The quintiles of the 90-day return show excess 5-day returns of +0.31 %, +2.26 %, -3.86 %, -0.04 % and -1.00 % from deepest to shallowest. In the deepest third of falls, days 2 to 5 rose +1.85 % above drift (t 2.10).
- **F4:** The book earns only on the first day of a position. Position gain is +0.158 % per bar on the first bar after entry (346 bars, sum +0.55). It is -0.237 % on the second bar (sum -0.82) and negative again from bar 6 onward (sum -0.60).
- **F5:** The book holds its shorts long after the bounce bar, and the losses come from those extra days. Of 3,323 short bars, 2,900 were outside the bounce regime. Those bars lost -1.46 in summed gain, against +0.64 on the regime bars. The 28 trades held 10 to 30 days lost -27.7 % on average and the 46 held 5.5 to 10 days lost -10.6 %, against -0.30 % for the 294 held about 5 days. Overall, the 660 trades lost -4.04 % on average, with 28.8 % winners.
- **F6:** The 5-day move is smaller than the cost of a trade, but the next-day move is not. Over 5 days the unusual move per case is -0.10 % against a cost of 0.22 % (-0.4 times the cost). The next-day giveback is -0.58 % (about 2.6 times the cost) and -2.33 % after bounces above 4 usual moves.
- **F7:** The 5-day aftermath depends on the year, while the next-day giveback is negative in 7 of 8 years. Days 2 to 5 fell -4.83 % in 2022 (t -3.18) and rose +7.6 %, +3.3 % and +3.6 % in 2020, 2021 and 2024 (t 2.39, 2.31 and 2.33).

## Ideas
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.d1_big-bounces-fade-next-day` (from F1, F2, F4, F6): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise measured in usual daily moves, the larger its fall over the next 1 day.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.d2_bounce-size-sets-giveback` (from F2, F3, F7): In a coin whose 90-day return is negative, the larger its one-day rise measured in usual daily moves, the larger its fall over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
