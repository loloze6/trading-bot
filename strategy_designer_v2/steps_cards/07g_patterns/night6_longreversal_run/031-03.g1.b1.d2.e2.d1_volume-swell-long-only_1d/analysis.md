---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only_1d
idea tested: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4318 USD
---
## Findings
- **F1:** The 14-day over 30-day volume ratio ranks the next 14-day excess return almost in order across its quintiles: -4.4 % (t -2.2, 306 cases on 80 days), -1.9 %, +1.6 %, +0.7 %, +5.1 % (t 1.74, 78 days). The drying side, which the book never shorts, is the only quintile beyond |t| 2, and it is barely there after the many angles looked at.
- **F2:** The bars on which the book was flat (forecast at or below 0) were followed by a 14-day excess return of -1.6 % (t -1.3, 1303 cases on 186 days). That is too weak to support a short side on volume drying.
- **F3:** The brief's own situation, the 60-day move, shows no lean against the earlier move over the next 14 days. Excess returns by 60-day return quintile are +0.7 %, -0.9 %, +1.2 %, +0.4 %, +1.1 %, all with |t| ≤ 0.38. The volatility-scaled 60-day move shows the same, with every |t| ≤ 0.54.
- **F4:** Shorter past moves lean with momentum rather than reversal, but not reliably. The 28-day return quintiles give -1.8 %, -2.5 %, -1.0 %, +2.7 %, +2.7 % over the next 14 days, with the largest t at 1.3 in absolute value. The 14-day return's top quintile gives +3.3 % (t 1.27).
- **F5:** The weekday effect fades once the coins of one day are taken together. Saturday's excess daily return of +0.32 % has t 2.0 on 414 days, but no year reaches t 1.5 (2022 is -0.12 %). Wednesday's +0.19 % has t 0.78.
- **F6:** The bounce after a large down day does not hold up once counted by day. After a day below -2 of its usual move, the next day's excess return is +0.21 % (t 0.65, 278 days). After -2 to -1 it is +0.19 % (t 1.0). The bounce shows only in 2018-2021 (+0.79 %, t 2.04, 330 days) and is gone in 2022-2025 (-0.17 %, t -0.91).
- **F7:** There is no reversal over 3 days either. The 3-day excess return after 3-day moves, by quintile, ranges from -0.51 % to +0.07 %, with every |t| ≤ 1.57.
- **F8:** The tested idea itself is uneven over time. Its 14-day excess return is negative in 2018 (-6.8 %), 2022 (-6.0 %, t -2.35) and 2025 (-3.1 %), and positive in 2020, 2021, 2023 and 2024 (+2.7 % to +5.3 %, each |t| ≤ 1.1). The book's largest-loss decile days coincide with coin falls of -6.4 %, so its losses are the market's falls taken while long.

## Ideas
- No ideas: Across the volume ratio, the 60-, 28- and 14-day moves, volatility, distance from the 50-day mean, next-day and 3-day reversals, weekdays and years, no pattern apart from the tested idea's own volume gradient stands out from chance (the best clustered t's are near 2 among roughly fifty looks), so no finding supports a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
