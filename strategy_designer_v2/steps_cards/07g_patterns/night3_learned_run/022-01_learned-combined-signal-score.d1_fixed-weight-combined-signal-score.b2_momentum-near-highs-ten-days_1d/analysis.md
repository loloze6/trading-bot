---
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4385 USD
---
## Findings
- **F1:** Next-day returns are higher on Thursdays and Fridays than on Mondays and Wednesdays, net of each coin's drift: Thursday +0.25 % (t 2.6), Friday +0.30 % (t 3.8), Monday −0.24 % (t −2.5), Wednesday −0.30 % (t −2.7), about 2,480 days each. The Thu+Fri minus Mon+Wed gap is positive on all 6 coins (+0.16 % to +0.36 % per day, t 1.7 to 3.1, about 1,657 days each) and in 6 of 8 years (2019 t 7.5, 2024 t 2.9), with 2022 slightly negative (t −0.5). It stands out among the roughly 15 angles looked at.
- **F2:** The tested forecast's slope does not carry forward evenly. Over windows w1 to w12 it is −0.00077 (t −0.75, 696 cases); over w13 to w24 it is +0.0042 (t 3.8, 707 cases). The pooled confirmation (t 2.7) rests on the later half, which is the brief's own test of whether what is learned carries forward.
- **F3:** The two components carry the same information rather than independent errors. Alone, the 28-day momentum has t 2.4 and the nearness to the 90-day high has t 2.6. Together in one regression they fall to t 0.96 and t 1.39 (1,691 cases), so the combination adds little over the better single effect.
- **F4:** The forecast's edge is concentrated in its top fifth: +2.04 % unusual 10-day move (t 2.0), against −0.41 % to +0.33 % in the middle three fifths and −1.26 % in the bottom fifth (t −1.8, 342 cases per fifth). The same shape appears for momentum alone (top +2.04 %) and for nearness alone (top +2.03 %).
- **F5:** The book earns on its long side only. Positions held long earn +0.082 % per bar before costs and short positions −0.007 %, although the book is short 49 % of the bars and long 49 %.
- **F6:** A large day in either direction is followed by a higher 10-day return than a quiet day. By fifth of the day's absolute move over the coin's 30-day volatility, the unusual 10-day move rises from −1.73 % (t −1.9) to +1.50 % (t 1.5), about 282 cases each. The gap of 3.2 % has Welch t of about 2.4, which is borderline given the number of angles.
- **F7:** In the highest third of 30-day volatility the forecast loses most of its strength. Its signed strength there is 0.007, against 0.094 and 0.124 in the low and middle thirds (about 465 cases each). However, the continuous interaction is not distinguishable from chance (t −0.9).

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.g1_learned-weekday-return-seasonality` (from F1): The higher a coin's average next-day return on the same weekday over its past 52 weeks, the higher its return over the next day.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.g2_big-days-precede-rises` (from F6): The larger a coin's last daily move in either direction, relative to its 30-day volatility, the higher its return over the next 10 days.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.g3_strong-momentum-near-highs` (from F4, F5, F3): The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, by more the further both sit above their usual levels.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
