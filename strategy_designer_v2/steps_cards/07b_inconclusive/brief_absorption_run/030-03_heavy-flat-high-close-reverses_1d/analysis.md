---
line: 7.b inconclusive
backtest: 030-03_heavy-flat-high-close-reverses_1d
idea tested: 030-03_heavy-flat-high-close-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3415 USD
---
## Findings
- **F1:** The tested short side was on the wrong side of the result: on heavy (volume ≥ 2x its prior 20-day mean) flat days, the 5-day unusual move after the bet's close was -0.74 % per case on the short side (t -0.94, 150 cases), so the coin rose more than its drift. Recomputed on the first heavy flat day of each 5-day cell, the move after a close in the top third of the range was +1.50 % (t 0.84, 43 cases), against +0.13 % after a close in the bottom third (40 cases), with a correlation of +0.12 between close location and the 5-day move.
- **F2:** Heavy-volume days that were not flat point the same way as F1, the opposite of the tested reversal, and more clearly: after a close in the top third of the range the unusual move was +1.75 % over 5 days (t 2.52, 323 cases) and +3.56 % over 10 days (t 3.07, 319 cases), against +0.13 % and +1.00 % after a close in the bottom third.
- **F3:** The link grows with volume and horizon. On a 10-day grid of all days with volume ≥ 2x the prior 20-day mean, the correlation of the 10-day unusual move is +0.09 with close location alone and +0.27 with close location x volume ratio (145 cases). The high-minus-low-close spread over 10 days is +14.9 % on days with volume ≥ 3x (t 1.33, 46 cases).
- **F4:** The flat-day effect is mixed across coins and years, which is why the main measure lands near zero. The correlation of close location with the 5-day move is +0.44 on LTC and +0.47 on ZEC but between -0.15 and +0.03 on BTC, ETH, XMR and XRP. By year, the 10-day high-minus-low spread on heavy days is +9.7 % to +16.0 % in 2018–2021 and +5.2 % in 2025, but -9.0 % (t -1.83) in 2022, -8.2 % (t -1.53) in 2023 and -4.3 % in 2024; no part of the data shows the tested reversal clearly.
- **F5:** The signal is rare: flat heavy days give 20–26 cases per coin, and the book was in a position on 6 % of coin-days. The continuation move in F2 (+3.56 % over 10 days) is many times the 0.19 % cost of a trade, while the tested short's total move (-1.35 %) loses about 7 times that cost.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation` (from F1, F2, F3, F5): On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 10 days, and the effect is larger the heavier that day's volume is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
