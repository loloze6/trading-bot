---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
idea tested: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4187 USD
---
## Findings
- **F1:** The tested effect sits almost entirely in the earlier years. In the trending regime (90-day return above 0), the slope of the demeaned 5-day return on the close's position in its 30-day range is +0.068 (t 4.65, 689 grid cases) over 2018–2021 and +0.001 (t 0.10, 623 cases) over 2022–2025. By year, 2020 alone has t 4.80, and 2022–2025 each have |t| < 0.6.
- **F2:** The tested effect is uneven across coins. The trending range-position slope is positive with t 1.83–2.75 for XRPUSD, ZECUSD, BTCUSD and ETHUSD, but −0.008 (t −0.30, 203 cases) for LTCUSD and +0.011 (t 0.58, 234 cases) for XMRUSD.
- **F3:** In the unknown regime (90-day return at or below 0), strength reverses after 2021. Over 2022–2025 the slope of the demeaned 5-day return on the 20-day return in units of 20-day daily volatility is −0.0158 (t −4.55, 721 cases), and on the 30-day range position it is −0.030 (t −2.96, 654 cases). Over 2018–2021 the same slopes are +0.0072 (t 1.65) and +0.030 (t 2.15), so the pooled slope is only −0.0037 (t −1.33).
- **F4:** Inside the trending regime, recent strength of any length precedes more rise over the next 5 days. Slopes of the demeaned 5-day return: 1-day return in volatility units 0.0094 (t 3.15), 5-day 0.0087 (t 2.86), 20-day 0.0096 (t 3.33), over 1549 / 1549 / 1465 cases. The same slopes in the unknown regime have |t| ≤ 1.33.
- **F5:** In the trending regime, the 5-day move is lopsided across range quintiles. The top range quintile is followed by +1.14 % demeaned (t 1.99, 495 cases) and the second-lowest by −1.44 % (t −2.39, 186 cases). The unknown regime shows no quintile with |t| > 0.6.
- **F6:** Saturdays stand out. The cross-coin mean Saturday return is +0.45 % (t 3.04, 414 days), the largest of the 7 weekdays, and Saturday minus other days is positive in 7 of 8 years, though no single year passes t 1.63 on day means. This is a weekday condition, not a graded situation, so no idea is drawn from it.
- **F7:** The book's gain comes from long holds and long trades:

## Ideas
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers.g1_bounce-fades-in-fallers` (from F3): In a coin whose 90-day return is negative, the larger its 20-day return measured in units of its daily volatility, the more it falls over the next 5 days, and the deeper it has fallen the more it rises back.
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers.g2_risers-strong-days-continue` (from F4, F5): In a coin whose 90-day return is positive, the larger its last day's return measured in units of its daily volatility, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
