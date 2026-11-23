---
line: 7.d confirmed, not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6407 USD
---
## Findings
- **F1:** The Calmar failed because the yearly return is small, not because the falls are deep: the book earns +3.0 % a year over 7.94 years with a deepest fall of only 5.2 % (Calmar 0.576), a slow 258-day slide from w12 to w14, while it sits in a position on just 13 % of the coins' days.
- **F2:** The gain is concentrated in the strongest cases of the idea's own grading. By |forecast| quartile, the book's 12-bar gain per case rises from 0.0001 to 0.0013, 0.0063 and 0.0094 (105 cases each). By weekend-over-weekday volume quartile, the signed 12-bar move is 0.0025, 0.0025 and 0.0042, then 0.0142 in the top quartile (mean ratio 2.51). By move-size quartile it is 0.0033, 0.0002 and 0.0077, then 0.0122 in the top quartile (z 2.08).
- **F3:** The short side carries the effect. After heavy weekend falls the signed 12-bar move is +0.97 % (t 2.62, 171 cases) and the book gains 0.0072 per case (t 3.16). After heavy weekend rises it is +0.32 % (t 1.24, 248 cases), with a book gain of 0.0022.
- **F4:** Heavy weekend moves in the direction of the coin's 30-day return continue by 0.76 % over 12 bars (t 2.84, 278 cases), against 0.24 % (t 0.68, 141 cases) when they go against it. The condition alone earns nothing: on light weekends, 30-day agreement gives −0.08 % (t −0.68, 995 cases) and disagreement 0.00 % (844 cases). So it belongs to the idea rather than being an effect of its own.
- **F5:** A Sunday pullback against the weekend move strengthens the continuation: 1.23 % (t 3.35, 132 cases) against 0.29 % (t 1.09, 287 cases) when Sunday went the same way. But the condition alone earns 0.51 % (t 3.06, 453 cases) on light weekends, so it is largely a separate effect and is not used as a repair.
- **F6:** The sizing puts its largest positions where the effect is weakest. In the calmest quartile of the coin's usual move the mean allocation is 0.86, but the move is only 0.11 %. The two middle quartiles carry 1.43 % and 0.86 % with allocations near 0.46. The most volatile quartile gives −0.06 %.
- **F7:** Changing the exit adds little. The 6-, 12- and 24-bar moves are 0.35 % (t 2.07), 0.58 % (t 2.73) and 0.58 % (t 1.83). Stops at −2 %, −3 % and −5 % lift the mean per case only from 0.58 % to 0.62 %, 0.69 % and 0.67 %.
- **F8:** The losses cluster in 2025. That year holds 10 of the 15 worst weeks, and its cases average only 0.08 %. The worst weeks had larger weekend moves than the average case (z 1.71 against 0.97) and weaker agreement with the 30-day trend (0.080 against 0.119).

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend` (from F4, F2, F8, F1): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays, and in the same direction as its 30-day return, continues in that direction over the first 12 hours of Monday. The continuation is the larger the larger the move and the heavier the weekend volume against the weekdays.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue` (from F3, F1): A coin's Saturday-Sunday fall made on higher volume than its mean over the preceding five weekdays continues downward over the first 12 hours of Monday. The continuation is the larger the larger the fall and the heavier the weekend volume against the weekdays.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation` (from F2, F6, F1): A coin's Saturday-Sunday move made on weekend volume a multiple of its mean over the preceding five weekdays continues in the same direction over the first 12 hours of Monday. The continuation grows steeply with how many times heavier the weekend volume is than the weekdays, and with the size of the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
