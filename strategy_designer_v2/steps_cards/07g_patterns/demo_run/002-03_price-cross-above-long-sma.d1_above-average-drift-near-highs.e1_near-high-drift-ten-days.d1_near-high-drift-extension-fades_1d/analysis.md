---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3615 USD
---
## Findings
- **F1:** Above the 200-day average, the 10-day return minus the coin's mean rises with the close's place in its 20-day close range: +0.0335 in the top fifth of the range (t 2.56, 268 non-overlapping cases) against -0.0312 in the bottom fifth (t -2.86, 123 cases).
- **F2:** Below the 200-day average the same range position shows no gradient: the five bins run from -0.023 to +0.001, every |t| ≤ 1.3, so the range effect appears only in the uptrend regime.
- **F3:** Above the 200-day average, the next 10 days rise with the past 30-day return rather than fading after it: the lowest two quintiles give -0.028 (t -1.27, n 43) and -0.029 (t -2.53, n 88), and the highest two give +0.018 (t 1.54, n 168) and +0.022 (t 1.53, n 222). This is the opposite of the plan's extension penalty.
- **F4:** The recorded forecast itself barely sorts the next 10 days on trending bars: its top quintile gives +0.014 (t 0.97) and its bottom quintile +0.004 (t 0.45). The 60-bar standardisation and the cubic penalty appear to have blurred the plain range and momentum effects in F1 and F3.
- **F5:** The book loses most when it is positioned against strong moves: on its worst 2% of days (348) it lost 10.5% on average while the coin rose 7.9%, and on its best 2% it gained 9.4% while the coin fell 4.8%.
- **F6:** Long-held trades do the damage: the 109 trades held over 30 days lost 30.0% each on average, -3272 summed, against -663 for the 1270 trades held 3–10 days.
- **F7:** The weekday pattern is not strong enough to count, given how many angles were checked and that coins share the same days: Friday's next-day excess return is +0.0030 (t 3.76, n 2479) and Wednesday's is -0.0030 (t -2.70), with mixed signs across the rest of the week.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.g1_uptrend-range-position-drift` (from F1, F2, F4): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.g2_uptrend-thirty-day-momentum-continuation` (from F3, F4, F5): While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
