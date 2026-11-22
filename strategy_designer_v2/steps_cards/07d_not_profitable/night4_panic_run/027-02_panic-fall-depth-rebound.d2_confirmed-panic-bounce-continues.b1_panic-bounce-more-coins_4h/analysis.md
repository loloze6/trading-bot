---
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4227 USD
---
## Findings
- **F1:** Holding the coin is what fails the book: it is in a position on only 21.7 % of coin-days, earns 0.0055 % a day on the other 29,164 coin-days where the coins rose 0.079 % a day, and earns 0.090 % a day on its 8,091 in-position days where the coins rose 0.41 % a day; the result is a mean of 0.014 % a day and a Sharpe 0.31 below holding's.
- **F2:** The bounce carries no graded premium: over 428 panic cases, the excess 84-bar return by bounce quintile goes +0.4 %, −1.0 %, −2.2 %, +0.4 %, +2.6 % (slope t 1.47), and the two lowest quintiles, which the forecast's clip at 0 leaves flat, still had a total 14-day move of +3.3 % and +1.6 %.
- **F3:** The 30-day move before the panic grades what follows better than the bounce does: the slope of the excess 14-day return on the absolute prior 30-day return is t 2.19 on 345 cases; by quartile of that absolute move the excess goes −3.3 %, −0.2 %, +2.9 %, +3.5 % (total −0.5 % to +6.5 %).
- **F4:** That premium sits at both ends of the prior move: the most-down quintile of the prior 30-day return has +2.8 % excess and the most-up has +4.8 %, while the middle quintiles have −2.3 % and −2.2 %; the signed slope is weaker (t 1.58).
- **F5:** The Calmar failure (0.099) comes from one long fall of −37.8 %: the chained book drops by −32 % to −38 % across w14–w20, starting in w14 where the book lost 0.196 % a day against the coins' −0.43 %, whereas no window before w14 falls deeper than −17.8 %.
- **F6:** Cost is not the cause: the cases' total move of +1.68 % is 7.5 times the 0.22 % cost of a trade and the 1,092 trades net +3.43 % each (t 3.5, held 13.8 days), but the unusual move per case is −1.28 % (strength −0.041), so the book earns the coins' drift on a fifth of the days and no premium.
- **F7:** Larger panics lean higher: the top quartile of the range multiple has +2.0 % excess against −0.2 % to −1.1 % in the other three (slope t 1.47 on 428 cases).

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.d1_panic-after-large-monthly-move` (from F3, F4, F2, F6): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's absolute 30-day return before the stretch, in either direction, the higher its return over the following 14 days.
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.d2_bounce-after-large-monthly-move` (from F3, F2, F1, F5): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 14 days, only while the coin's absolute 30-day return before the stretch is large, the effect growing with that 30-day move.
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.d3_panic-size-sets-premium` (from F7, F2, F6): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the range's multiple of its 30-day average, the higher the coin's return over the following 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
