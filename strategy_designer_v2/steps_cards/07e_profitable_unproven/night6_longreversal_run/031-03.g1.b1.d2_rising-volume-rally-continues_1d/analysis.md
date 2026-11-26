---
line: 7.e profitable but not proven
backtest: 031-03.g1.b1.d2_rising-volume-rally-continues_1d
idea tested: 031-03.g1.b1.d2_rising-volume-rally-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4482 USD
---
## Findings
- **F1:** The book's mean daily return of 0.0749 % (t 3.13 over 2898 days) splits about evenly between the market's own rise and timing: 0.0379 % comes from the positions held times the coins' mean daily return, and only 0.0370 % comes from timing.
- **F2:** The gain sits in a few years and a few trades: the book's mean daily return was +0.22 % in 2020, +0.17 % in 2023 and +0.21 % in 2024, but negative in 2018 (−0.06 %), 2022 (−0.05 %) and 2025 (−0.01 %); the top 5 % of the 3848 trades carry 66 % of the summed trade profit (median trade +2.1 %).
- **F3:** No single coin carries the book: XRP (15 %), DOGE (12 %) and ADA (12 %) are the largest shares of the gain, and 18 of 19 coins contribute positively.
- **F4:** On the 14-day grid the volume swell sorts the next 14-day excess return as strongly when the 14-day return is down as when it is up: the Spearman correlation of the swell with the excess return is 0.167 in up-moves (763 cases) and 0.163 in down-moves; across down-move terciles the excess return runs −3.4 % (t −1.75, 74 days), +0.8 %, +1.9 %.
- **F5:** The clearest part of the effect is the losing side, which the book never trades. In up-moves with volume at or below its 30-day mean, the next 14 days are −3.9 % below the coin's normal (331 cases, plain t −3.93). The lowest swell tercile of up-moves is −3.8 % (day-clustered t −2.16, 68 days). The top tercile, the one the book buys, is +6.1 % (clustered t 1.93, 72 days).
- **F6:** In 14-day up-moves, cases with volume above its 30-day mean beat those without in 84 % of the coins (16 of 19). They also beat them in 6 of 8 years: by +9.6 % in 2021, +7.7 % in 2023 and +18.5 % in 2024.
- **F7:** The 14-day return alone carries no 14-day effect (Spearman −0.001 over 1530 cases). The volume part does: at 7 days the top swell tercile in up-moves earns +2.5 % (clustered t 2.03, 173 days), and the lowest down-move tercile loses −2.3 % (clustered t −2.13).

## Ideas
- `031-03.g1.b1.d2.e1_rally-on-fading-volume-fails` (from F5, F6, F1): The more a coin's mean daily volume over the last 14 days falls below its mean daily volume over the last 30 days while its 14-day return is up, the more its price falls relative to its normal drift over the next 14 days.
- `031-03.g1.b1.d2.e2_volume-swell-predicts-rise` (from F4, F7, F6): The more a coin's mean daily volume over the last 14 days sits above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, whatever the sign of its 14-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
