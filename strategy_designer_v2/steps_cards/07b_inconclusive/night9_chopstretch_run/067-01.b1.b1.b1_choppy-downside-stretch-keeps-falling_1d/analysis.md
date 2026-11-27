---
line: 7.b inconclusive
backtest: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling_1d
idea tested: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3902 USD
---
## Findings
- **F1:** The verdict's slope is on the other side of the idea and near zero (slope −0.00039, t −0.56 clustered by day, 405 cases on 228 days). In folds B and C, the forecast<0 cases repeat this: slope on the forecast +0.0016, t 0.68, n 128; slope on the raw stretch +0.015, t 0.96. Deeper stretches below the average are not followed by clearly larger falls than shallow ones.
- **F2:** The forecast buckets below the average are not graded. Excess 5-day returns are −1.8 % (−2 to 0), −2.4 % (−5 to −2), −1.1 % (−10 to −5), −8.5 % (−15 to −10, t −3.39, n 28) and +0.4 % (−20 to −15, n 20). The supporting check's −1.06 % on forecast ≤ −10 rests on one bucket, and the deepest one reverses it.
- **F3:** The carry shows across the average, not inside one side. On all choppy grid cases in folds B and C, the excess 5-day return rises with the raw two-sided stretch (r 0.205, t 3.29, n 249; clustered slope +0.0094, t 1.82). Below-average bands give −6.7 %, −5.2 %, −1.8 % and −1.6 %; above-average bands give +1.3 %, −1.2 % and +1.3 %. On one side alone the slope is weak: below t 0.96 (n 128), above t 0.85 (n 121).
- **F4:** The two-sided relation holds at every horizon tested (clustered t 1.66 at 1 day, 2.94 at 2 days, 1.73 at 3 days, 1.82 at 5 days, 2.33 at 10 days). It is strongest over 10 days, with excess +4.9 % in the top band (stretch above +2.5) against −4.0 % to −7.7 % in the two lowest bands. The 10-day returns are read on a 5-day grid, so they overlap and the 2.33 is optimistic.
- **F5:** The two-sided relation points the same way on all six coins: the stretch-to-excess correlation is 0.05 to 0.43 (BTC 0.26, XRP 0.43, ZEC 0.22). Choppy cases more than 1.5 usual moves below the average are followed by −1.4 % to −9.8 % excess over 5 days on every coin.
- **F6:** The idea's size is small against the market's drift. Its unusual move is +0.60 % per case (t 1.50, 449 days; 0.071 of a 10.6 % usual move), but the coins' normal drift works against the short by −0.57 %, so the total move is +0.03 %, 0.1 times the 0.19 % cost of a trade. A short-only book cannot pay even if the effect is real. The unusual move is 3.1 times the cost.
- **F7:** Outside the choppy profile, the stretch does not carry in a graded way. Its lowest sextile gives +0.1 % excess over 5 days (n 196) and the next one −2.7 % (t −3.88). The upper sextiles give +1.6 % to +2.0 %, flat across them. The graded carry belongs to the choppy situation.

## Ideas
- `067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries` (from F1, F3, F4, F5, F6, F7): In a choppy market, a coin's close above or below its 20-day average, measured in units of its 20-day standard deviation of daily returns, is followed by a move the same way over the next 10 days. The further the close stands from the average on either side, the larger that move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
