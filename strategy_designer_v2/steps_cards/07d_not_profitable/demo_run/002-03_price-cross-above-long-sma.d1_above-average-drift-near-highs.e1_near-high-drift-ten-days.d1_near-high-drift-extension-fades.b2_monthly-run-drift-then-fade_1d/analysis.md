---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5579 USD
---
## Findings
- **F1:** The short side earns nothing and the long side carries the whole book. In the trending regime, short bars average a gain of 0.000174 per bar (t 0.53, n 2535, mean allocation −0.27), while long bars average 0.001244 (t 4.71, n 5918, mean allocation 0.41). Across all bars, shorts summed 0.43 against 7.38 for longs.
- **F2:** Shorts deepen the falls that sink Calmar. The deepest fall is in w5 (−24.5%, the worst 20-day book sum −0.124). There shorts lost −0.58 against −0.29 for longs, and XRP alone lost −0.67 while its price rose 0.33. In 2023, shorts lost −0.639 while the coins' mean daily return was +0.0015 and the book's was −0.000192.
- **F3:** The coins do drift down after a negative 30-day run above the 200-day average, but only against their own average. Trending grid cases with a 30-day return ≤ 0 have a 10-day excess return of −0.024 (t −2.39, n 175). Shorting them still yields almost nothing (F1), because the coins' mean rise offsets the shortfall.
- **F4:** The fade at extreme runs is real in the raw 30-day return but missed by the standardised forecast. On trending grid cases with a positive 30-day return, the 10-day excess return is +0.044 (t 1.84) in the 26–45% quintile and −0.006 (t −0.24) above 45%. Long bars with a 30-day return above 40% gain 0.000189 per bar against 0.001998 for 7–40%, yet they still hold an allocation of 0.38 against 0.50. Meanwhile the standardised s ≥ 14 bucket shows no fade (s≥14 minus 8≤s<14: −0.0095, t −0.38).
- **F5:** The book's worst days come from large longs held after big runs. On the worst 5% of book days, the book is long on 68% of coin-bars (32% on other days), with mean allocation 0.26 (0.09), mean 30-day return 0.23 (0.04) and mean s 9.4 (6.3).
- **F6:** Among trending cases with a positive 30-day return, the gain shows up mostly where the 10-day run is also strongest. The top 10-day-return quartile has a 10-day excess return of +0.049 (t 2.18, n 114), while the other quartiles lie between −0.001 and +0.014 (|t| ≤ 1.13).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.d1_long-only-monthly-run-drift` (from F1, F2, F3): While a coin's close is above its 200-day average and its 30-day return is positive, the larger that 30-day return, the larger its rise over the next 10 days, except at its very largest 30-day returns, where the larger that return, the smaller the rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.d2_raw-run-fade-above-average` (from F4, F5): While a coin's close is above its 200-day average, the larger its 30-day percent gain, the larger its rise over the next 10 days, except where that gain is largest as a share of the price itself, where the larger the 30-day percent gain, the smaller the rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.d3_fresh-run-carries-drift` (from F6, F1): While a coin's close is above its 200-day average and its 30-day return is positive, the larger its 10-day return, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
