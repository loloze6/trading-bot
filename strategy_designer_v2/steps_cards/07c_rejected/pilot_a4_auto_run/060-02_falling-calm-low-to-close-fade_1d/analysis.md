---
line: 7.c no effect
backtest: 060-02_falling-calm-low-to-close-fade_1d
idea tested: 060-02_falling-calm-low-to-close-fade
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3905 USD
---
## Findings
- **F1:** The tested fade is not in the data. Over all windows, the short cases' unusual move was +0.18 % per case (t 0.36, 98 days, 150 cases), only 0.043 of a usual 4.83 % daily move, and the total move of +0.14 % is 0.4 times the 0.33 % cost of a trade.
- **F2:** On the explore half's falling-calm days (477 days, BTC, XMR and DOGE), the next-day move does not grade with how far the close stands above the low. The Spearman correlation is −0.024, the five quintiles of that distance give −0.30 %, +0.15 %, −0.67 %, +0.79 % and −0.19 % with no t beyond ±1.4, and the top quintile's −0.19 % (t −0.37, 96 cases) is no fall.
- **F3:** The brief's own combination, width against the 30-day swing times nearness of the close to the high, does not grade the next day either. Its Spearman correlation is −0.024 at 1 day and −0.023 at 5 days, and its top quartile moves −0.10 % the next day (t −0.22, 119 cases) and −0.66 % over 2 days (t −0.81, 60 cases).
- **F4:** The few strongest cases in the explore half did fall, but the full test erases this. The 22 days at 2 usual moves or more fell 1.55 % more than usual the next day (t −2.27), while all windows give +0.18 % with t 0.36 for 150 cases. The fall in these 22 days is a small-sample artefact, not a stable effect.
- **F5:** What the market did instead was continue up after a strong up day, over a few days. In the top quartile of the day's return against its 30-day swing, the coin rose 5.16 % more than usual over the next 5 days (t 2.26, 19 non-overlapping cases), and 5.86 % in the top quintile (t 2.40, 16 cases). The correlation of the day's scaled return with the forward move climbs with the horizon: −0.074 at 1 day, +0.029 at 5 days, +0.059 at 10 days.
- **F6:** That continuation follows a small give-back the next day. The top quartile of the day's scaled return moves −0.88 % the next day (t −1.82, 119 cases) before the 5-day rise. A 1-day horizon therefore measured the idea in the one place where the move runs against the continuation.
- **F7:** The 5-day continuation points the same way on every coin and in every year with cases, though its strength is uneven:

## Ideas
- `060-02.c1_falling-calm-surge-continuation` (from F5, F6, F7, F1, F2, F3): In a falling, calm market, a day that closes far above the previous day's close against the coin's 30-day daily swing is followed by a rise over the next five days. The rise is larger the larger that day's gain against the swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
