---
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4816 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.69 against 0.75). Two long falls cause it: −23.7 % over about 500 days from w10, while the coins rose +20 to +23 %, and −17.0 % over 387 days from w21 (2024–2025), while the coins rose +51 %. The case gains in those years were 2018 +0.03 % (t 0.05), 2021 −0.19 % (t −0.32) and 2025 −0.59 % (t −1.66), against +0.57 % to +1.39 % in 2019, 2020 and 2022–2024.
- **F2:** The effect lives in calm markets and is absent in turbulent ones. In the low tercile of a coin's 30-day hourly volatility, the Monday–Tuesday move in Saturday's direction averages +1.04 % (t 5.0, 750 cases). In the middle tercile it is +0.30 % (t 1.28, 747) and in the high tercile −0.04 % (t −0.12, 749). The 5 % worst adverse path over the 48 hours goes from −8.1 % in the low tercile to −19.9 % in the high one.
- **F3:** Low volatility is not an effect of its own. The coins' unsigned 48-hour return on those same Monday bars is only +0.09 % in the low tercile, against +1.04 % when Saturday's sign is followed. It belongs to the brief's own theory: a weekend move made on thin books stands as information when the market is orderly, and is noise when the market is moving violently anyway.
- **F4:** A weekly book that trades only the low-volatility tercile has a Calmar of 1.82 (deepest fall −5.2 %, yearly +9.4 %, weekly Sharpe 1.23). Low and middle terciles together give Calmar 0.97 (deepest fall −13.3 %, yearly +12.9 %). The full book gives Calmar 0.70 (−24.4 %, +17.1 %).
- **F5:** The effect is concentrated in the strongest cases. The top quintile of |forecast| earns +1.63 % per case (t 4.23, 485 cases), while the four lower quintiles earn only +0.07 % to +0.30 % (t 0.19 to 0.98). Trading only the top two quintiles gives Calmar 0.78 against 0.70.
- **F6:** Sunday's move carries much of the information, and it is a separate effect that cannot repair this book. On Mondays where Sunday moved against Saturday, following Saturday earns +0.96 % (t 4.57, 1320 cases), and following it when Sunday agreed earns −0.10 % (t −0.47). Fading the last 24 hours at Monday 00:00, without Saturday's signal, already earns +0.58 % (t 3.81, 2387). At the other weekdays' midnights the same fade earns between −0.33 % and +0.16 %.
- **F7:** Dropping a side does not help. Shorts earn +0.65 % per case (t 2.71) and longs +0.35 % (t 1.85), but a short-only book has a Calmar of only 0.32.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets` (from F1, F2, F3, F4): A coin's 24-hour return over Saturday is followed over the next two days, Monday and Tuesday, by a move in the same direction that grows with the size of Saturday's move. This holds only while the coin's 30-day volatility of hourly returns is low against its own past year, and the calmer the coin, the larger the continuation.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue` (from F5, F2): A coin's 24-hour return over Saturday, measured against the coin's usual 30-day move, is followed over the next two days by a move in the same direction. That continuation grows faster than in proportion to Saturday's move, so Saturday's largest moves carry most of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
