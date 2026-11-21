---
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
idea tested: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3570 USD
---
## Findings
- **F1:** The book earns a mean 0.000278 a day against 0.00118 for holding the coins, and its gain comes from its longs alone: long bars sum +5.75 (+0.000617 a bar), short bars sum −0.76 (−0.000109 a bar), and 524 short trades lose a mean 5.1 % after fees, with 34 % winners.
- **F2:** The shorts lose because a close far beneath the 90-day high is still followed by a rise. Grid cases with a negative forecast gain +1.6 % over 20 days (416 cases, excess t −0.85), against +3.4 % for positive forecasts (411 cases, excess t 0.59). So the forecast's lower half bets against the coins' drift.
- **F3:** The forecast's information sits in its top fifth only. The top forecast quintile earns +0.00116 a bar on a mean allocation of 0.31; quintiles 1 to 3 earn between −0.00006 and +0.00025, and the bottom quintile is followed by a coin return of +0.0015 a day.
- **F4:** Longs pay only while the close is above its 50-day average. There they earn +0.000909 a bar on 4266 bars, with the coin returning +0.0018 a day. Below that average they lose −0.000049 a bar on 1709 bars, with the coin returning −0.0014 a day.
- **F5:** The book's falls are falls the coin shares while the book is long. On its 30 worst days the book lost a mean 3.5 % while the coins fell 9.5 %, and the coins were down on 100 % of them. The deepest fall is 18 %, against a yearly return that gives a Calmar of 0.53.
- **F6:** The idea's size is not what fails. Its total move per case is 3.39 %, 17.6 times the 0.19 % cost of a trade. But the book is small: mean absolute allocation is 0.19 and mean net allocation 0.067, with 40 % of bars short. That is too little exposure to reach a mean daily return of 0.0005.
- **F7:** The 20-day return grades what follows, on both forecast sides. Among positive-forecast grid cases, the 20-day return that follows rises with the past 20-day return, from +1.4 % in the second quartile to +3.6 % in the third and +6.3 % in the top (129 cases). In the top quartile even negative forecasts are followed by +4.5 % (42 cases).

## Ideas
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high.d1_nearness-above-fifty-day-average` (from F1, F4, F5): The closer a coin's daily close stands to its highest close of the previous 90 days, the more it rises over the next 20 days, only while its daily close stands above its 50-day average close.
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high.d2_nearness-strengthened-by-momentum` (from F2, F3, F7): The closer a coin's daily close stands to its highest close of the previous 90 days, the more it rises over the next 20 days, and the more so the larger its 20-day return.
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high.d3_twenty-day-momentum-continuation` (from F2, F6, F7): The larger a coin's 20-day return, the more it rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
