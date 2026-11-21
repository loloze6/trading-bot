---
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d
idea tested: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4207 USD
---
## Findings
- **F1:** The short side causes every failed measure. Shorts held for 13,447 bars and lost a mean -0.177 % per bar; longs held for 12,029 bars and gained +0.136 % per bar. Summed bar gains are -23.8 for shorts and +16.4 for longs. Closed trades after fees average -25.3 % on 1,340 shorts and +12.1 % on 994 longs.
- **F2:** Most of the shorts' loss is the coin's own rise, not bad timing. The market part is -0.112 % per bar and the timing part only -0.065 % per bar. The book was short more often (46 % of bars) than long (42 %) in coins whose mean drift is up.
- **F3:** Short losses concentrate in coins that had already risen strongly. When the 60-day return was in its top fifth (mean +97 %), shorts lost -0.92 % per bar while the coin rose +0.40 % per bar; in the fourth fifth (+23 %) they lost -0.32 % per bar. In the three lower fifths shorts sat between -0.09 % and +0.01 % per bar. Longs in the top fifth gained +0.31 % per bar.
- **F4:** The falls come from a few explosive windows where the book held shorts. Short losses summed -7.5 in w17, -6.8 in w6, -6.4 in w21 and -3.3 in w19. The book's daily standard deviation was 9.8 % in w17 and 11.1 % in w19, against 0.6 % to 3.7 % elsewhere. Its mean daily return was -0.75 % in w17 and -1.18 % in w19.
- **F5:** On the 20-day grid, the signal works better when it points the same way as the coin's past 20-day move. With |forecast| ≥ 2, the signed excess 20-day move is +4.7 % over 181 such cases, against +1.9 % over 331 cases where it points against it.
- **F6:** On the 20-day grid, the coin's own 60-day return carries a weak continuation. After the two lowest fifths of 60-day return, the next 20-day excess move is -3.0 % (t -1.48) and -3.7 % (t -1.95), 131 cases each. After the highest fifth it is +2.5 % (t 0.90), 131 cases.
- **F7:** The term pays when an extreme is read on the grid, not when it first appears.

## Ideas
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d1_weighted-reversal-with-trend-agreement` (from F1, F2, F3, F4, F5): When a coin's 1-day return, scored against its past 365 days and weighted by how well it predicted the following 5 days' return over those 365 days, is far from its usual value, the coin moves in that term's direction over the next 20 days, and the further out the term, the larger the move. The move is larger still the more the coin's own 60-day return points in the term's direction.
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues` (from F3, F6): The larger a coin's 60-day return, the more the coin moves in that same direction over the next 20 days.
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d3_persistent-weighted-reversal-extremes` (from F7, F1): When a coin's 1-day return, scored against its past 365 days and weighted by how well it predicted the following 5 days' return over those 365 days, is far from its usual value, the coin moves in that term's direction over the next 20 days, and the further out the term, the larger the move. The move is larger the more days of the past 20 days the term has stayed far out on the same side.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
