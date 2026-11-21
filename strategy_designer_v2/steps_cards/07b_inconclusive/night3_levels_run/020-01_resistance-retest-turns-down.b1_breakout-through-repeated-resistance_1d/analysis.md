---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4580 USD
---
## Findings
- **F1:** The effect is on the predicted side but tiny. The 10-day excess return per case is +0.31 % (t 0.62, 1084 cases), a strength of 0.009 of the coin's usual 14.49 % move, against about 0.05 for real ideas so far (findings F10). At this size, t 2 would need about (2 / 0.62)² × 1084 ≈ 11,000 cases, about 10 times this test.
- **F2:** The grading the idea predicts is absent. The Spearman correlation between the entry forecast and the 10-day excess return is 0.013. The forecast quartiles give −0.21 %, +0.66 %, +0.93 % and +0.28 %, so the largest breaks do no better than the middle ones. The step-5 median split passes only narrowly (+0.59 %).
- **F3:** The effect is mixed across periods, and the market's own moves swamp it. The 10-day excess return is −3.7 % in 2018 (t −1.90) and −2.8 % in 2022 (t −2.85), against +2.6 % in 2020 (t 1.95) and +4.0 % in 2024 (t 2.66). Only 46.8 % of cases end above drift, and the per-case standard deviation (16.3 %) is about 50 times the mean.
- **F4:** The effect is mixed across coins. On the 10-day excess return, XRP (+1.9 %, t 1.12) and ZEC (+1.6 %, t 1.06) are on the predicted side, LTC is against it (−1.6 %, t −1.45), and BTC and XMR are near zero. No coin reaches t 2.
- **F5:** A longer horizon or an uptrend does not give a clean answer either. On non-overlapping 30-day cells the excess return is +1.4 % (t 0.82, 431 cases). After a positive 60-day return it is +6.6 % (t 1.37, 94 cases), against −1.3 % (t −0.36, 67 cases) after a negative one. Even inside the uptrend there is no grading: the forecast-to-return Spearman is 0.07, and the strongest 60-day rises do worst (−3.4 %).
- **F6:** The size covers a trade, but the book is not robust. The unusual move is 1.6 times the 0.19 % round-trip cost and the total move 7.7 times. The book's Sharpe is 0.76, which beats holding by 0.21, but it fails on Calmar (0.53 against 0.75), consistent with the year-to-year swings in F3.

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins` (from F1, F4, F6): When a coin closes above a price where it turned down several times in the past 90 days, having closed below it the day before, it tends to rise over the next 10 days, and the more times it turned down there before, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
