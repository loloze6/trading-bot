---
line: 7.b inconclusive
backtest: 072-02_choppy-deep-up-day-fade_1d
idea tested: 072-02_choppy-deep-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3424 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but just short of the bar: the depth-weighted short gain against holding is +0.29 % per case with t 1.87 (1691 cases on 1028 days), and its size is an unusual move of +0.22 % (t 1.47, 691 days), a strength of 0.057, the usual strength of real ideas; recomputed on folds B and C, the plan's measure gives t 1.81 (576 cases, 377 days).
- **F2:** On folds B and C the effect is graded as the idea says: the next-day short gain against holding falls steadily from the deepest fifth of choppy closes below the 20-day high to the shallowest, +1.55 %, +0.78 %, +0.36 %, +0.57 %, −0.63 % (about 115 cases each), and on the active up days the deepest third gains +0.77 % against +0.13 % for the shallowest.
- **F3:** The evidence is thin because it is concentrated: without window w16 (18 cases, depth-weighted gain 62.8 against −3.5 to +6.7 elsewhere), the plan's measure falls from t 1.81 to t 1.37 (563 cases, 366 days), and the weighted gain is negative in 5 of the 12 windows (w8, w10, w11, w17, w18).
- **F4:** It is present on every core coin except ZEC (weighted gain +0.17 against +1.10 to +6.64 for the other five; deep fifths +0.80 % to +3.02 % against −0.16 % for ZEC) and in every year from 2018 to 2021 (+1.0 to +5.2), so the problem is too few cases rather than an effect confined to one part of the data.
- **F5:** The up-day version the idea names is the clearer side, with a depth-weighted t of 2.00 on 253 cases against 0.96 on 319 down-day cases, and its deepest third reaches t 2.02 to 2.78 over horizons of 1 to 5 days. With only 52 to 253 non-overlapping cases per test, narrowing the idea would leave even fewer.
- **F6:** A trade costs 0.19 %, while the total move per case is +0.11 % (0.5 times that cost) and the unusual move is +0.22 % (1.2 times it). As tested, the book cannot pay (Sharpe 0.02, yearly return −0.1 %) whatever this test's verdict on whether the effect is real.

## Ideas
- `072-02.b1_choppy-deep-up-day-fade-more-coins` (from F1, F2, F3, F4, F5): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
