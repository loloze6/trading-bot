---
line: 7.g patterns
backtest: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins_1d
idea tested: 067-01.b1.b1.b2_choppy-stretch-carry-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4321 USD
---
## Findings
- **F1:** Inside the choppy profile (the detector's regime "unknown"), the 5-day unusual move after closes below the 20-day average is negative at every stretch level, but it is not graded: −5.55 % (t −2.75, 55 cases) below −2 usual moves, −1.23 % (t −0.85) from −2 to −1, −3.74 % (t −3.85) from −1 to −0.3, and −2.62 % (t −2.36, 43 cases) even at the average itself (−0.3 to +0.3), which reads as choppy periods running below the coin's all-window drift rather than as a stretch effect.
- **F2:** The 20-day range position inside the choppy profile tells the same story: the 5-day unusual move is −4.12 % (t −2.06, 60 cases) at the range bottom, −2.86 % (t −2.62) from 0.1 to 0.3 and −2.26 % (t −3.17, 98 cases) in the middle 0.3 to 0.7, so the low and the middle of the range fall alike.
- **F3:** With the cases of one day taken together, the choppy profile's carry is +5.07 % per case below the average (t 2.21, 93 cases on 46 days) and +5.48 % above it (t 1.23, 96 cases on 45 days). The graded carry, stretch times move, is t 1.79 on 76 days, below what stands out after the roughly 60 cells examined in rounds 1 and 2.
- **F4:** Outside the profile, in rising and falling markets, the carry is positive on both sides but never sure once the cases of one day are taken together: rising above +1.77 % (t 1.37), rising below +2.57 % (t 1.32), falling above +1.88 % (t 1.29), falling below +1.46 % (t 1.02), graded rising t 1.88 on 84 days. It is positive in every year from 2018 to 2021, at +0.55 % to +3.11 % and t 0.42 to 2.64, and continuation in rising markets is already held on the map (034-01.e1, 033-03.b2, 034-02).
- **F5:** In falling markets, closes more than 2 usual moves above the average are followed by a +4.05 % unusual 5-day move (t 2.64), but this rests on only 45 cases on 20 days, one cell among many examined.
- **F6:** The book's trades split by side: 568 long trades at a mean of +2.48 % net (median −0.34 %) against 747 short trades at −2.43 % (median −2.88 %). Trades of up to 5 days lose −2.06 % on average (813 trades), while those of 10 to 20 days gain +3.50 % (141) and those of 20 to 60 days gain +14.60 % (20), so the book's gain comes from the few stretches that persist.
- **F7:** The book's mean daily return is 0.015 % (1449 days, standard deviation 0.86 %). Its best 5 % of days add up to 7.4 times its total gain, and its windows range from −0.09 % (w10) to +0.18 % (w16) a day, with 6 of 12 windows negative.
- **F8:** The next-day unusual return by weekday is negative on Mondays in every year (−0.60, −0.62, −0.01, −0.34 % in 2018 to 2021) and positive on Fridays in 3 of 4 years. With the cases of one day taken together, neither is sure (Monday t −1.07, Friday t 1.47, about 206 days each).
- **F9:** After one-day shocks scaled by the 20-day swing, no profile shows a 2-day unusual move with a day-clustered t above 1.83 (the largest is choppy, middle shocks −1.14 %, t −1.82).

## Ideas
- No ideas: Across stretch, range position, one-day shocks, trend and volatility regimes, weekdays and the trades, no pattern both stands out from chance with the cases of one day taken together (the best are t 2.21 on 46 days and t 2.64 on 20 days, among about 60 cells) and is graded. The one consistent effect, continuation in rising markets, is already held on the profile map.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
