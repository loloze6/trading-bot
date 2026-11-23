---
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2274 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the mean signed unusual 48-hour move is +1.04 % with t 1.76 over 258 non-overlapping weekend cases. The sign holds at every horizon measured: +0.68 % at 12h (t 2.46), +0.69 % at 24h (t 1.63), +1.41 % at 72h (t 2.30) and +1.57 % at 96h (t 2.10, 257 cases).
- **F2:** The effect is mixed across coins, which drowns it at six coins. It is positive in ETH (+2.53 %, t 2.35, 40 cases), XRP (+6.10 %, t 2.19, 38 cases) and BTC (+2.19 %, t 1.80, 25 cases). It reverses in XMR (−2.14 %, t −2.70, 48 cases) and is near zero in LTC (−0.25 %, t −0.25) and ZEC (−0.10 %, t −0.09). With only 25 to 64 cases per coin, more coins would give the clear answer.
- **F3:** A minority of large cases carries much of the mean. The median case is +0.43 % and the 5 %-trimmed mean +0.57 %, against a mean of +1.04 %, and the hit rate is 53.5 %.
- **F4:** The grading is weak in the forecast as a whole but present in the volume. The Spearman correlation of |forecast| with the 48h unusual move is 0.001, and the |forecast| quartiles give +1.04 %, −0.39 %, +2.04 % and +1.48 %. By weekend-to-weekday volume ratio terciles the move rises from +0.39 % (t 0.32) to +1.44 % (t 1.46) to +1.74 % (t 1.64).
- **F5:** The falling side carries the effect. Weekend falls in a falling 30-day trend continue by +1.64 % signed (t 2.31, hit 67 %, 97 cases) at 48h and +1.67 % at 12h (t 3.55). Weekend rises in a rising trend give +0.67 % (t 0.80, hit 45 %, 161 cases).
- **F6:** The effect is not confined to one period. Six of the eight years are positive, with 2020 the strongest (+4.00 %, t 2.43, 44 cases), while 2018 (−1.51 %), 2023 (−0.57 %) and 2025 (−0.93 %) are negative.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation.b1_heavy-weekend-continuation-more-coins` (from F1, F2, F6): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours, the more so the larger the move and the heavier the weekend volume. The continuation is larger the more the weekend move goes the same way as the coin's 30-day return before the weekend.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation.b2_heavy-weekend-falls-keep-falling` (from F4, F5): A coin's Saturday-Sunday fall made on higher volume than its mean over the preceding five weekdays continues downward over the next 48 hours, the more so the heavier the weekend volume and the larger the fall, while the coin's 30-day return before the weekend is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
