---
line: 7.b inconclusive
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
idea tested: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4041 USD
---
## Findings
- **F1:** The positive result rests on a few extreme cases. Over the 277 grid cases the forecast-weighted mean 26-day excess return is +9.4 % (t 1.75), but the median excess return is -4.5 % and only 43 % of cases beat the coin's own mean. Removing the top and bottom 2 % of forecast-weighted products (265 cases left) cuts the weighted mean to +2.4 % with t 0.99.
- **F2:** The graded part of the idea is absent. The Spearman correlation between the cloud-slope forecast and the 26-day excess return is -0.027. Across the forecast quintiles the weighted means are +16.5 %, +3.4 %, +8.0 %, -4.2 % and +21.9 % (t 1.17, 0.49, 1.18, -1.13, 1.71), with no rise from slow to fast cloud rises. The coin's own past 26-day return does not sort the outcome either: the quartile means are +10.8 % to +19.2 %, with a Spearman of 0.025.
- **F3:** The effect sits in one year. In 2021 the 59 cases have a weighted mean of +41.9 % (t 2.01). Every other year is small or negative: 2023 +3.4 % (41 cases), 2024 +3.5 % (66 cases), 2025 +3.0 % (38 cases), 2020 -10.4 % (40 cases), 2022 -20.1 % (6 cases).
- **F4:** The effect also sits in a few small, volatile coins. DOGE shows +96 % over 13 cases and INJ +39 % over 7. The six default coins together show +3.8 % (t 0.91, 149 cases), and BTC, ETH, LTC and XMR each lie between +1.7 % and +6.8 % with t below 1.
- **F5:** As step 5 measures it, the idea is small. Its unusual move is +1.00 % per case over 26 days, a strength of 0.018 of the coin's usual 32.35 % move over 420 cases. That is well below the strength of about 0.05 that real ideas have shown (findings F10). Most of the +6.34 % total move per case is the coin's own drift of +5.35 %.
- **F6:** No more data is available for this test. It already used all 19 coins and all four folds on daily bars. Running the same idea on hourly bars would add no edge of its own (findings F3).

## Ideas
- No ideas: The above-rising-cloud effect comes from a few large 2021 moves in small, volatile coins (F1, F3, F4), not from a steady pattern. It is not graded by the cloud's slope (F2), its trimmed t is 0.99, and its strength is about a third of a real idea's (F5). No condition, side or horizon in this data isolates a graded effect, and no more data is available (F6), so the clear answer is that a coin trading above a rising cloud does not reliably keep rising beyond its usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
