---
line: 7.g patterns
backtest: 031-01_extreme-rise-partly-reverses_1d
idea tested: 031-01_extreme-rise-partly-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4043 USD
---
## Findings
- **F1:** The tested situation does not grade: among 102 non-overlapping 30-day cases with a recorded overreach value, the 30-day return minus the coin's drift barely moves with the vol-scaled 90-day rise (Spearman 0.005, p 0.96). The terciles run -1.62 % (t -0.34) at z 1.18, -1.44 % (t -0.30) at z 1.86 and +4.07 % (t 0.49) at z 4.40, so the largest rises lean on upward rather than back.
- **F2:** The book lost on every coin, with mean daily book returns from -0.014 % (LTC) to -0.157 % (BTC) while the coins gained +0.067 % to +0.188 % a day. It lost in 6 of 8 years and gained only in the two falling years, 2018 (+0.012 % vs coin -0.353 %) and 2022 (+0.027 % vs coin -0.180 %). The short paid only when the whole market fell, not after the coin's own overreach.
- **F3:** After a day whose return is in the lowest tenth of its 30-day volatility (mean z -1.78), the next day's return beats the coin's drift by +0.52 %. That is t 3.39 over 1,271 cases, but only t 1.90 with cases of one day taken together (472 days).
- **F4:** The F3 bounce is graded inside down days. The next-day excess return by quartile of down days runs +0.50 % (t 3.73, z -1.65), +0.08 % (z -0.74), +0.03 % (z -0.38) and -0.00 % (z -0.12). The Spearman correlation over all days is -0.074 (p ≈ 1e-16, not clustered by day).
- **F5:** The F3 bounce is positive on all six coins over the next day, from +0.17 % (ETH, t 0.45) to +1.12 % (XMR, t 3.57). It weakens with time, from +0.77 %, +0.55 %, +1.39 % and +0.88 % in 2018–2021 to +0.05 % in 2024 and +0.04 % in 2025. Over 3 days it is +1.07 % (t 2.28, day-clustered 1.44), carried mainly by XMR (t 3.51) and 2021 (t 3.56).
- **F6:** Saturday's return is +0.44 % (t 4.91 over 1,814 coin-days, not clustered by day) against -0.31 % on Thursday (t -2.46). Saturday is positive on all six coins (t 1.40 to 2.92) and in all 8 years, though near zero in 2018 (+0.11 %), 2022 (+0.07 %) and 2023 (-0.00 %).
- **F7:** Past-return momentum and reversal at 3 to 30 days show no graded lean: every Spearman correlation between the vol-scaled past return and the forward excess return lies between -0.023 and +0.049 (p ≥ 0.09). The isolated quintile t's near ±2.8 do not line up into a gradient.

## Ideas
- `031-01.g1_sharp-drop-next-day-bounce` (from F3, F4, F5): The further a coin's one-day fall stands below its own usual daily move (its 30-day volatility), the more it rises back over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
