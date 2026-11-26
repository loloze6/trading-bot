---
line: 7.b inconclusive
backtest: 031-01_up-streak-length-reversal_1d
idea tested: 031-01_up-streak-length-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4372 USD
---
## Findings
- **F1:** The graded part of the idea runs the wrong way, so the inconclusive result is mixed, not just small. In folds B and C at 5 days, up-close days whose streak ranks above 0.8 against the coin's past-year streaks were followed by rises beyond the drift: +2.6 % unusual (strength +0.19, t 1.99, 166 cases) for ranks 0.8–0.95 and +2.4 % (strength +0.22, t 2.07, 64 cases) above 0.95. Ranks at or below 0.5 were followed by falls of 1.3 % (strength −0.14, t −1.10, 80 cases). This matches step 5's failed supporting check (top third minus bottom third −0.17 % in the short direction).
- **F2:** The same continuation shows by forecast size. The top third of |forecast| had a long-direction strength of +0.18 (unusual +3.1 % raw mean return, t 2.56, 234 cases). The low and mid thirds were about zero (−0.01 and −0.02, t −0.18 and −0.39). So the strongest short signals are the ones most often wrong.
- **F3:** At 10 days the gradient is steeper and still continuation. Ranks above 0.95 gave strength +0.33 (unusual +5.0 %, t 2.50, 35 cases); ranks at or below 0.5 gave −0.46 (unusual −6.7 %, t −2.39, 40 cases). Another horizon does not rescue the reversal reading.
- **F4:** The continuation after long up streaks lives in rising markets (60-day return above +10 %). There, ranks above 0.8 gave strength +0.42 (unusual +5.6 %, t 2.23, 64 cases) against +0.07 (t 0.79, 96 cases) for shorter streaks. In choppy markets both groups were near zero (−0.02 and −0.05). In falling markets the effect was weaker (+0.19, t 1.67, 44 cases, against +0.00).
- **F5:** Calm markets carry the up-day continuation: strength +0.20 (unusual +2.3 %, t 2.89, 208 cases). Agitated markets were flat: −0.00 (t −0.02, 95 cases).
- **F6:** The effect splits by period and coin, which blurs the pooled measure.
- **F7:** The test's main measure is on the idea's side but small and far from the bar. The unusual short move was +0.32 % per case, t 1.08 over 1,206 days, strength 0.035 against a usual 5-day move of 10.6 %. Twelve more coins exist in folds A and D and partly in B and C that the test did not use. F1 to F4 suggest more data would mainly sharpen the continuation gradient.

## Ideas
- `031-01.b3_up-streak-reversal-all-coins` (from F7): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it falls over the next 5 days.
- `031-01.b4_rising-market-up-streak-continuation` (from F1, F2, F3, F4): In a rising market, the more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 5 days.
- `031-01.b5_calm-market-up-streak-continuation` (from F1, F2, F5): In a calm market, the more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
