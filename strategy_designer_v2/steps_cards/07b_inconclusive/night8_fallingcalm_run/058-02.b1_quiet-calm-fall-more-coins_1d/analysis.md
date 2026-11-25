---
line: 7.b inconclusive
backtest: 058-02.b1_quiet-calm-fall-more-coins_1d
idea tested: 058-02.b1_quiet-calm-fall-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5801 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side but far short of the bar: per-case mean 0.0046 with a day-clustered t of 0.67 over 907 cases on 263 days. The grading it rests on fails: the larger-|forecast| half beats the smaller half by -0.0035 % (supporting check failed). In the explored folds the forecast quartiles go -0.44 %, +2.07 %, +0.56 %, +1.42 % (small to large), a Spearman of 0.05.
- **F2:** The fall's depth is not graded the way the idea needs. Among the cases, the 5-day short-direction unusual move is +0.53 % (t 0.31) for the deepest third of 30-day falls, +2.71 % (t 2.25) for the middle third and -0.21 % (t -0.12) for the shallowest. The product of depth and volume therefore spreads the forecast over a part that carries no order.
- **F3:** The volume part is graded. Inside the falling calm profile, after a 30-day fall, the unusual move is +3.24 % (t 1.42, 35 cases) when 30-day volume is lightest against the past year, +1.25 % (t 0.78) in the middle and -1.88 % (t -0.91) when heaviest. Deep falls on heavy volume go the other way, at -4.60 % (t -2.24, 18 cases), against +3.33 % for deep falls on quiet volume.
- **F4:** The same volume gradient shows outside the falling calm profile, after 30-day falls. The unusual move is +3.21 % for the quiet third (t 1.22), +3.04 % for the middle third (t 1.81) and -0.53 % for the heavy third (t -0.09). Deep and quiet gives +5.75 % (t 2.26), deep and heavy -1.19 %. The quiet-volume continuation is therefore not confined to the calm downtrend, and restricting to it halves the cases.
- **F5:** The effect is mixed across periods and drowned by the coins' own rise. The unusual move is +2.29 % in 2018 and +2.09 % in 2019, but -6.56 % in 2020 (t -2.44) and -1.00 % in 2021. The coins' normal 5-day drift in the short direction is -0.87 %, which leaves a total move of +0.04 % per case. That is 0.3 times the 0.22 % cost of a trade.
- **F6:** Changing the horizon does not clarify the result. The cases' unusual move is -0.27 % over 1 day, -0.36 % over 3 days, +0.91 % over 5, +0.83 % over 10 and +1.49 % over 20, all with t under 1. No more data is available, because the test already used every coin and fold on daily bars.

## Ideas
- `058-02.b1.b1_quiet-volume-fall-keeps-falling` (from F2, F3, F4): After a 30-day fall, the lighter a coin's volume over those 30 days compared with its own average volume over the past year, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
