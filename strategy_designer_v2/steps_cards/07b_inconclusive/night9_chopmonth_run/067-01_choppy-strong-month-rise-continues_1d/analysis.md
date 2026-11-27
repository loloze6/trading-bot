---
line: 7.b inconclusive
backtest: 067-01_choppy-strong-month-rise-continues_1d
idea tested: 067-01_choppy-strong-month-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3731 USD
---
## Findings
- **F1:** The tested side shows no grading in folds B and C. On choppy 7-day grid cells with a positive 30-day return, the slope of the 7-day excess return on the 30-day return is negative: t -1.02 on 136 cells in round 1, and t -0.81 on 104 cells in round 2. The mean excess is +0.8 % (t 0.75), which matches step 5's slope t of 0.86 with an unusual move of +0.55 % (t 0.95, 572 days).
- **F2:** The effect lives on the falling side. On choppy 7-day cells with a 30-day return at or below 0, the slope of the 7-day excess return on the 30-day return is t 3.93 on 111 cells. The mean excess return in the fall's direction is +5.1 %, with a day-clustered t of 2.82 over 54 days.
- **F3:** The falling-side effect is graded across the deciles of the 30-day return in choppy markets. The mean 7-day excess is -10.5 % after a mean month of -31 %, -8.3 % after -21 %, -4.6 % after -13 % and -4.2 % after -6 %. Above -2 % it is near 0 (+0.5 %).
- **F4:** The falling-side effect is broad. The 7-day excess after a non-positive month in a choppy market is negative on all 12 coins, from -1.3 % on BTC to -10.6 % on DOGE. It is negative in 8 of 12 windows, for example -24 % in w16, -7.6 % in w12 (26 cells) and -10.5 % in w18.
- **F5:** The effect is clearest over 7 to 10 days. The falling-side slope t is 3.93 at 7 days and 5.40 at 10 days (83 cells), then 2.16 at 14 days. The rising side reaches t 1.25 at 10 days and 1.97 at 14 days, and the day-clustered t of its mean is under 1.1 at every horizon.
- **F6:** The tested idea's own side is mixed across windows. The mean 7-day excess after a positive month runs from +14.6 % in w18 and +10.4 % in w10 to -12.8 % in w14 and -16.4 % in w7.

## Ideas
- `067-01.b1_choppy-weak-month-keeps-falling` (from F2, F3, F4, F5, F1): In a choppy market, the larger a coin's fall over the past 30 days, the more it falls over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
