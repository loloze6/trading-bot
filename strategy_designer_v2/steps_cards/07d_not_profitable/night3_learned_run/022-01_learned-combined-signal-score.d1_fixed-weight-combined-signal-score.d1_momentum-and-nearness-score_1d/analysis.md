---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3791 USD
---
## Findings
- **F1:** The book fails on its mean daily return of 0.000343 against the required 0.0005, and on a Calmar of 0.43 against 0.75. Holding the coins earned 0.00118 a day, and the book's deepest fall is 27.2 %, lasting 485 days, over which the book lost 29 % while holding the coins gained 46 %.
- **F2:** The long side carries the whole gain and the short side causes the falls. The long bars summed +7.15 against −0.69 for the short bars, with fees of 0.30 and 0.25. On its own, the long side's daily chain earns 0.000408 a day, 14.9 % a year, with a deepest fall of 12.3 % (a Calmar of about 1.2). The short side's chain earns −0.000042 a day, −2.2 % a year, with a deepest fall of 31.1 %.
- **F3:** On the non-overlapping 5-day grid, a positive score is followed by +1.06 % over 5 days (t 3.73, 1652 cases). After a negative score the coin still rises, so the short loses 0.14 % (t −0.57, 1767 cases). The idea's confirmed slope therefore comes from the upper side of the score.
- **F4:** The most negative scores are followed by rises rather than falls. In the lowest forecast decile the coin's next-day return is +0.23 %, against +0.36 % and +0.43 % in the two highest deciles and −0.14 % in decile 2.
- **F5:** Deep falls below the 90-day high are followed by rebounds.
- **F6:** Long positions pay most while the coin's 30-day volatility is low against its own history. In the lowest volatility quartile a long bar earned 0.00139 a day, with a next-day coin return of +0.51 %. In the other three quartiles it earned 0.00034 to 0.00068.
- **F7:** Cost is not the cause. Per case, the total move of +0.89 % is 4.6 times the 0.19 % round trip, in line with the earlier finding (F11) that ideas larger than their cost can pay. What loses is the side the move goes against, the shorts.

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.d1_combined-score-upper-side` (from F1, F2, F3, F4, F7): When a coin's 28-day return and its closeness to its 90-day high are combined into one score, each weighted equally in its known direction, the coin's return over the next 5 days is higher the higher that score is, only while the score points up (the coin has risen over 28 days and sits nearer its 90-day high than usual).
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.d2_rebound-below-90-day-high` (from F4, F5): The further a coin's close sits below its 90-day closing high, the higher the coin's return over the next 5 days.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score.d3_combined-score-in-calm` (from F2, F6, F7): When a coin's 28-day return and its closeness to its 90-day high are combined into one score, each weighted equally in its known direction, the coin's return over the next 5 days is higher the higher that score is, and the more so the lower the coin's 30-day volatility sits against its own history.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
