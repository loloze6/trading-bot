---
line: 7.g patterns
backtest: 059-01_swing-scaled-rise-continues_1d
idea tested: 059-01_swing-scaled-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3839 USD
---
## Findings
- **F1:** The tested continuation lives only in calm markets: on the 5-day grid of folds B and C, signed excess returns after the forecast average +2.36 % per case in calm coin-days (642 cases, t 4.03 with the cases of one day taken together, 159 days), against −0.07 % in agitated ones (1068 cases, t −0.10, 263 days). Here calm means a 30-day swing at or below the coin's median.
- **F2:** Inside calm markets the effect is graded and holds under every trend: the slope of excess return on the forecast is 0.0024 in falling calm (t 3.43, n 152), 0.0038 in choppy calm (t 3.94, n 98) and 0.0035 in rising calm (t 3.69, n 179). In agitated markets it is 0.0003 when falling (t 0.42) and 0.0008 when rising (t 0.53). The calm forecast quintiles climb from −3.57 % (t −4.07) to +2.99 % (t 2.74).
- **F3:** The calm-market slope is positive in every year: 2018 t 1.75, 2019 t 1.27, 2020 t 3.17, 2021 t 1.80. It is positive on every coin, with t from 1.55 (XMR) to 3.86 (ETH). The agitated-market slope is negative or zero in every year (t −1.15, −0.70, +0.10, −0.38).
- **F4:** The continuation weakens steadily as the coin's swing rises. By the coin's own volatility tercile, the slope is 0.0022 in the lowest (t 5.53, n 426), 0.0016 in the middle (t 3.65) and −0.0007 in the highest (t −1.18). Dividing the forecast by the coin's swing relative to its usual swing raises the pooled slope t from 3.05 to 5.37.
- **F5:** The book earns where the idea works. On calm coin-days its mean daily return is +0.215 % (t 4.51, 3301 coin-days) against +0.124 % for holding. On agitated coin-days it is +0.043 % (t 1.13, 5388 coin-days) against +0.142 % for holding. In 2021 the book's Sharpe was 0.39 against holding's 1.48.
- **F6:** A single day's move measured against the coin's 20-day swing also continues over the next 5 days.
- **F7:** The next-day return after Thursdays and Fridays is positive: +0.61 % (t 4.10) and +0.52 % (t 3.87). This repeats the late-week gain the profile map already holds (045-01), so it is left out.

## Ideas
- `059-01.g1_calm-swing-scaled-move-continues` (from F1, F2, F3, F5): In a calm market, the larger a coin's 20-day move measured in units of its own daily swing over those 20 days, the further it moves the same way over the next 5 days, up after a rise and down after a fall.
- `059-01.g2_calmer-scaled-move-carries-further` (from F2, F4): The larger a coin's 20-day move in units of its own 20-day daily swing, and the calmer its last 30 days against its own past year, the further it moves the same way over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.g3_calm-one-day-shock-continues` (from F6): In a calm market, the larger a coin's one-day move measured in units of its daily swing over the previous 20 days, the further it moves the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
