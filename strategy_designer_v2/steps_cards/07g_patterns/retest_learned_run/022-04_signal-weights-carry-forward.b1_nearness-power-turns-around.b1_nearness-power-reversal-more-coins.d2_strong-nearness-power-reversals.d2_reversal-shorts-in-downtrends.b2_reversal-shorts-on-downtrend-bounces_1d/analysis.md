---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6343 USD
---
## Findings
- **F1:** The tested shorts look strong case by case but much weaker once each date counts once: across the 293 active grid cases the excess 5-day return is −0.175 usual moves (t −3.55, −2.01 % per case), but averaging same-date cases first gives t −1.29 over 144 dates, and the main measure falls to t −1.27 over 144 dates. Most of the confirmation's t comes from several coins moving together on the same dates.
- **F2:** The tested shorts' edge sits in 2025: that year's 106 cases show −0.342 usual moves (t −4.11, −3.85 %), while all other years together give a date-clustered t of −0.49 for the excess move and −0.66 for the main product, over 115 dates and 187 cases.
- **F3:** The joint reading barely sorts the outcome inside the gate: the most negative forecast quartile shows −0.247 (t −2.45, n 74) and the least negative −0.118 (t −1.30, n 73). On bounce bars where the forecast was 0, the fall is only −0.052 (t −1.22, n 422).
- **F4:** The largest 5-day rises inside a 20-day fall are followed by falls case by case: the top quintile shows −0.148 usual moves (t −3.07, −1.62 %, n 395). By bounce-size quartile the excess move goes +0.005, −0.095, −0.147, −0.175. But the date-clustered slope on the 5-day return is t 0.70 over 215 dates inside the bounce gate, and t 0.05 over 396 dates across all 20-day falls, so the gradient does not hold up as independent evidence.
- **F5:** The weekday pattern looks large case by case but not by date: Tuesday shows +0.191 (t 4.29, n 653) and Sunday −0.208 (t −5.40, n 680), yet date-clustered these are t 1.06 (86 dates) and t −0.99 (88 dates). The book's daily return by weekday (−3.0 to +2.1 bp) shows no matching pattern.
- **F6:** Grouping by other variables gave no monotone and robust pattern: the past 1-, 20- and 60-day returns, the 20-day to 120-day volatility ratio, and nearness to the 90-day high (quintiles) show isolated quintiles at |t| ≈ 2.3–3.5 in no consistent order. Out of about 40 groups tested, that is what chance alone would produce.

## Ideas
- No ideas: Across the forecast, the gate, past returns, volatility, nearness, weekday and year, every pattern that stood out case by case (F1, F4, F5) loses its significance when same-date cases across coins are counted once, or rests on 2025 alone (F2), so none stands out enough to support a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
