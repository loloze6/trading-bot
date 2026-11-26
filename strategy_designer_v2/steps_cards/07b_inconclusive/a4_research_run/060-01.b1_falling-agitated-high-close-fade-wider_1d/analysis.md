---
line: 7.b inconclusive
backtest: 060-01.b1_falling-agitated-high-close-fade-wider_1d
idea tested: 060-01.b1_falling-agitated-high-close-fade-wider
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1920 USD
---
## Findings
- **F1:** The grading the idea predicts is absent: on the 169 bars in a short (mean_reversion, inside the falling-agitated profile), the short's next-day unusual move falls as the close nears the high, +0.73 % for closes in 0.5–0.75 of the range (n 84, t 1.20), +0.57 % in 0.75–0.9 (n 55, t 0.78) and +0.55 % in 0.9–1.0 (n 30, t 0.36); by |forecast| quartile it is +1.20 %, +0.55 %, +1.17 % and −0.36 % (t −0.30) for the strongest quarter.
- **F2:** The effect does not belong to the profile: outside it (chop regime), upper-half closes give the short a similar next-day unusual move of +0.46 % for closes in 0.5–0.75 (n 532, t 1.56) and +0.31 % for 0.75–0.9 (n 345, t 0.85), against the profile's +0.73 % and +0.57 %, so the brief's own falsifier ("as strong outside falling agitated markets") is close to met.
- **F3:** The small positive result rests on one coin and on the early years: ZEC carries it (+1.09 %, n 125, t 2.16) while BCH is flat (+0.05 %, n 34, t 0.05) and DOGE is negative (−2.87 %, n 10, t −0.95); by year it fades from +2.98 % in 2018 (n 25, t 2.34) and +1.01 % in 2019 (n 38, t 2.03) to +0.06 % in 2020 (n 61, t 0.08) and −0.17 % in 2021 (n 45, t −0.14).
- **F4:** Another horizon does not reveal the effect: the short's unusual move over 1, 2, 3 and 5 days is +0.65 % (t 1.39), +0.10 % (t 0.15), +0.49 % (t 0.69) and +1.23 % (t 1.37) on 169 to 161 cases (overlapping beyond 1 day, so the longer t's are overstated), with no horizon clear of t 2.
- **F5:** The test already used all the daily data the idea can run on (19 coins, folds A to D, 534 distinct days), and its main measure, +0.30 % weighted with day-clustered t 1.01, is a sixth of a usual daily move (5.16 %) and, as a total move of +0.27 %, below the 0.32 % cost of a trade.

## Ideas
- No ideas: The theme's effect is not in the data: no more daily data is available, the next-day fade after an upper-range close is ungraded or inverted in the strongest cases (F1), it is about as present outside the falling-agitated profile (F2), and it fades across years and coins (F3) with no horizon where it shows (F4), so no amendment on the theme has a finding to rest on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
