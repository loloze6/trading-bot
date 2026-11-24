---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g1_midweek-run-carries-into-saturday_1d
idea tested: 031-01.g1.g1_midweek-run-carries-into-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3841 USD
---
## Findings
- **F1:** The check failed on Calmar (0.247 against 0.75), and the falls come from the short side. A rebuilt book with 0.19 % cost per trade earns +5.6 %/yr with a deepest fall of −23.6 % (Calmar 0.24, Sharpe 0.56). Its long Saturdays alone earn +9.1 %/yr with a deepest fall of −9.0 % (Calmar 1.00, Sharpe 1.12). Its short Saturdays alone earn −3.3 %/yr with a deepest fall of −31.6 %.
- **F2:** The effect is one-sided by side. Long Fridays give a signed unusual Saturday move of +0.65 % (t 5.47, 1197 cases), rising through the forecast quartiles from +0.14 % to +1.00 % (t 3.73). Short Fridays give +0.02 % (t 0.17, 1279 cases) and lose 0.014 % a case before fees. The weakest short quartile goes the wrong way, at −0.65 % (t −2.47).
- **F3:** The book's deepest falls sit in windows w5 to w10, where the deepest fall reaches −23.5 % in w9.
- **F4:** Part of the short side's loss is Saturday's own drift. All Fridays give a Saturday unusual move of +0.30 % (t 3.76, 2479 cases), so going long on Saturday is a condition that alone earns about half of the long cases' +0.65 %. The long side still adds +0.35 % over that, and its grading holds.
- **F5:** Shorts work only near the yearly low.
- **F6:** Rising cases pay across the whole range: +0.79 % (t 3.49) in the bottom third, +0.68 % (t 3.00) in the middle, +1.13 % (t 3.52) in the top. The top third alone, without the signal, gives +0.81 % (t 3.69), so a condition on the top of the range would be its own effect and is left out.
- **F7:** Friday's own move does not carry the grading. Cases where Friday agrees with the Monday-to-Thursday side earn +0.30 % (t 2.65), and cases where it opposes earn +0.35 % (t 3.00).

## Ideas
- `031-01.g1.g1.d1_midweek-gain-lifts-saturday` (from F1, F2, F3, F4, F7): The higher a coin's return over the four days from Monday's close to Thursday's close, the more it rises over Saturday (UTC), and this grading does not come from Friday's own move, taken on its rising side only: the larger the Monday-to-Thursday gain, the larger Saturday's rise.
- `031-01.g1.g1.d2_midweek-fall-near-yearly-low` (from F1, F3, F5, F6): The higher a coin's return over the four days from Monday's close to Thursday's close, the more it rises over Saturday (UTC), and this grading does not come from Friday's own move. A Monday-to-Thursday fall is followed by a Saturday fall only while the coin trades in the lower part of its past-year range, and the larger that fall, the larger Saturday's decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
