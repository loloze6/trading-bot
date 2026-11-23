---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4497 USD
---
## Findings
- **F1:** Inside the regime where the 20-day return is positive, grid cases with a positive forecast earn an excess 5-day return of +0.34 % (917 cases), against +0.18 % for those with a zero forecast (1103 cases). Welch t is 0.30, so the nearness-power reading adds nothing measurable on top of the regime it runs in.
- **F2:** The regime does more than the forecast. Grid cases after a 20-day rise have an excess 5-day return of +0.25 % (2020 cases), against −0.35 % after a 20-day fall (1976 cases), Welch t 1.76. The book also loses less than holding in falling years (2018: −0.027 % a day against −0.361 %; 2022: −0.044 % against −0.194 %). It earns less than holding in rising years (2020: +0.110 % against +0.423 %; 2021: +0.057 % against +0.425 %). The book's Sharpe looks like a trend-gated, part-time exposure to the coin's drift, not timing.
- **F3:** Nearness to the 30-day high is not graded. The top decile shows +1.53 % excess over 5 days (t 2.12, 363 cases) and the third decile −1.42 % (t −3.14), but the rank correlation over all grid cases is 0.016 (p 0.33). The top-20 % mean swings by year from +8.3 % (2021) to −2.0 % (2025).
- **F4:** The last day's return gives no graded 5-day effect. Its quintiles alternate in sign (+0.82 %, −1.20 %, +0.25 %, −0.87 %, +0.78 % excess). The 20-day and 60-day quintiles are not monotone either (60-day: −0.03 %, −1.07 %, +0.71 %, +0.07 %, +0.47 %).
- **F5:** The 20-day volatility level separates nothing. All five quintiles have |t| ≤ 0.84 for the excess 5-day return, and the volatility tercile crossed with the 20-day sign has every cell at |t| ≤ 1.81.
- **F6:** The next day's excess return depends on the weekday of the decision close, but as a fixed calendar on-off, not a graded effect.

## Ideas
- No ideas: Across the forecast, the regime, past returns at 1, 5, 20 and 60 days, nearness to the 30-day high, volatility, weekdays, years and the book's daily returns, nothing stands out as a graded per-coin effect. The only sharp pattern is a weekday calendar (F6), which is a fixed on-off condition whose t is inflated by pooling correlated coins on the same days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
