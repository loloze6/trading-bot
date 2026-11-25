---
line: 7.g patterns
backtest: 054-01.b1_reclaimed-low-all-coins_1d
idea tested: 054-01.b1_reclaimed-low-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6545 USD
---
## Findings
- **F1:** In choppy markets (60-day return between -10 % and +10 %), the coin's 5-day excess return rises with its 20-day return scaled by its 30-day daily swing: slope +0.051 per unit (OLS t 7.37, not clustered by day, Spearman 0.30, 259 grid cases); it holds when agitated (slope +0.053, t 3.36, 101 cases) and when calm (slope +0.043, t 5.60, 158 cases).
- **F2:** The same grading is weaker in rising markets (slope +0.017, t 2.89, 424 cases) and absent in falling markets (slope +0.007, t 1.16, 478 cases), so this continuation lives in choppy markets.
- **F3:** Inside choppy markets the effect is monotonic across quartiles of the raw 20-day return: 5-day excess -6.3 % (t -2.27, 80 cases, 55 days), -2.0 %, -1.1 %, then +3.6 % (t 1.58, 81 cases). On the swing-scaled measure, the weakest quartile is negative in every year (2018 -5.1 %, 2019 -2.9 %, 2020 -16.3 %, 2021 -2.8 %) and on 5 of the 6 coins with enough cases.
- **F4:** Choppy agitated bars as a whole are followed by a 5-day excess of -5.2 % (t -2.63, 112 cases, 85 days). Their swing-scaled 20-day quartiles run from -6.9 % (q0) to -1.8 % (q3), so the falls come mostly from coins already down over 20 days.
- **F5:** The brief's situation is not in these folds. A reclaimed 30-day-low pierce in falling agitated bars gives a 5-day excess of +0.5 % (t 0.21, 39 cases, 22 days). Its deeper half does worse than its shallower half (-2.2 % vs +3.6 %), against the idea's grading. Over all markets, reclaimed pierces give -2.2 % (t -1.10, 163 cases), with no ordering by depth tercile (+0.1 %, -3.7 %, -2.4 %).
- **F6:** Days trading above the prior 30-day high are followed by positive 5-day excess (held break +3.5 %, t 2.96, 224 cases; rising calm +4.0 %, t 2.68; choppy calm +7.1 %, t 2.45, 33 cases). This repeats breakout and nearness-to-high ideas the profile map already holds (034-01.e1, 033-03.b2, 035-01.b1), so it is not a discovery.
- **F7:** The book's own mean_reversion bars give +5.4 % 5-day excess (t 1.45, 45 cases, 23 days), not distinguishable from 0, and the book held a position on only 3 % of the coins' days.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `054-01.b1.g1_choppy-market-20-day-continuation` (from F1, F2, F3, F4): In a choppy market, a coin keeps moving over the next 5 days in the direction of its 20-day return, and the move is larger the larger that 20-day return is measured in the coin's own daily swing over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
