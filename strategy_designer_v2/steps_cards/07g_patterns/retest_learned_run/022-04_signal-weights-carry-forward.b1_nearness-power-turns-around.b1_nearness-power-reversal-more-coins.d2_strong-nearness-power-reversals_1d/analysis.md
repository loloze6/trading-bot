---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4196 USD
---
## Findings
- **F1:** The tested forecast sorts what follows it, but weakly. Its quintiles run from −0.21 % (lowest) to +0.75 % (highest) in drift-removed 5-day return, with a rank-slope t of 2.44 over 4732 grid cases. Per coin the slopes are mostly small and not significant: the highest is LTC at t 1.76, the lowest TRX at t −1.89. This agrees with the step-5 strength of 0.007.
- **F2:** The grid's start weekday looked strong: Tuesday +2.14 % with t 4.30 over 644 cases, and Sunday −2.39 % with t −5.70 over 671 cases. Counted on every bar and grouped by date, so coins moving together count once, the effect is gone. Tuesday becomes +0.20 % (t 0.46) and Sunday −0.46 % (t −0.98) over about 400 dates each. The first reading came from coins moving together on the same dates.
- **F3:** Grouped by date, the coins' daily drift-removed return by weekday shows only Saturday standing out: +0.37 % with t 2.43 over 414 days. It weakens from +0.57 % (t 2.21) in 2018–2021 to +0.17 % (t 1.05) in 2022–2025. With seven weekdays tested, this does not stand out from chance.
- **F4:** Large days do not reverse over the next 5 days, grouped by date. After days below −2 usual daily moves the next 5 days return +0.21 % (t 0.11, 33 dates). After days above +2 they return +1.74 % (t 1.10, 62 dates).
- **F5:** Abnormal volume does not predict the next 5 days. Unsigned, no volume bucket reaches |t| 1.41. Signed in the direction of the day's move, none reaches t 1.34.
- **F6:** The 5-day momentum and 20-day momentum quintiles give rank-slope t of −2.13 and 1.42 without grouping by date. The 60-day-high nearness and 20-day volatility quintiles give 1.54 and 0.58. Volatility terciles do not change the 20-day momentum slope: t −0.00, 0.69 and 0.70. Given the inflation shown in F2, none of these stands out.
- **F7:** The book's worst 5 % of days average −3.37 % and come with a coin excess of −1.19%. Its best 5 % average +3.50 % with a coin excess of +1.25 % (144 days each). Its extreme days are carried symmetrically by the market's own large moves: the book is long 46 % and short 42 % of the time.
- **F8:** The book's mean daily return changes sign from year to year, from −0.072 % in 2022 to +0.128 % in 2019, with no link to the coins' mean daily return in the same year.

## Ideas
- No ideas: I looked at the forecast, momentum, nearness, volatility, large-day reversals, volume, weekday, year and the book's extreme days. Once coins moving together on the same date were counted once, no pattern beyond the tested idea's own weak slope stood out from chance.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
