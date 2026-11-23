---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4078 USD
---
## Findings
- **F1:** The effect is on the side the idea predicts. Its weakness comes from the weighting by forecast size, not from the shorts themselves. Unweighted, the 1,031 non-overlapping short cases fall 0.99 % beyond drift over 5 days (t 3.31). Weighted by abs(forecast), the step-5 measure gives 0.71 % (t 1.70).
- **F2:** The grading fails at the top. Case falls by forecast quintile are 0.76 %, 1.28 %, 1.37 % and 1.33 % (t 1.2 to 2.0). The largest quintile, with mean abs(forecast) 19.0, falls only 0.20 % (t 0.30). The slope is +0.00041 and the correlation of abs(forecast) with the fall is -0.03. The heaviest weights therefore sit on the cases that move least.
- **F3:** The test measured the idea at a shorter horizon than where it shows. The drift-removed fall after shorts grows with the horizon: 0.64 % over 1 day (t 4.67), 0.99 % over 5 days (t 3.31), 2.04 % over 10 days (t 4.81, 989 cases) and 3.55 % over 20 days (t 5.26, 907 cases). The 10- and 20-day returns are read on the 5-day grid, so they overlap and their t's are overstated, roughly by the square root of 2 to 4.
- **F4:** Within falling coins (20-day return below 0), the active shorts are followed by a fall the flat bars do not show. Over 5 days the shorts fall 0.87 % (t 2.68, 833 cases) against -0.12 % for the flat bars (1,141 cases), a difference of 1.00 % with Welch t 2.21. Over 20 days the shorts fall 3.51 % (t 4.41, 709 cases) against -0.40 % for the flat bars. So the signal, not the downtrend alone, carries the fall.
- **F5:** The effect is uneven across years. On the case grid it is strong in 2018–2020 (+2.6 %, +2.4 % and +2.8 % per 5 days, t 1.5 to 1.8) and in 2025 (+1.16 %, t 2.10). It is near zero in 2021–2024 (+0.55 %, +1.17 %, -0.29 %, +0.59 %). Across coins it is mostly positive but individually insignificant; only XRP reaches t 2.45. The test already uses every coin and fold available on daily bars, so no more data exists to add cases.
- **F6:** At 5 days the move barely pays for trading. The total move per case is +0.50 %, against a cost of 0.23 % per trade, because the coins' normal drift of -0.71 % works against the shorts. The book loses: Sharpe -0.05, mean daily return on days in a position -0.0066 %. The 20-day fall of F3 is about 7 times larger than the 5-day unusual move, against the same single trade cost.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.b1_nearness-reversal-over-20-days` (from F3, F4, F6, F1): For a coin's nearness to its 90-day high, the larger both the excess past power of that signal for the coin's 5-day returns over the past 365 days and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 20 days, only while the coin's 20-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
