---
line: 7.b inconclusive
backtest: 032-03.b1.b1_thin-volume-decline-all-coins_1d
idea tested: 032-03.b1.b1_thin-volume-decline-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4156 USD
---
## Findings
- **F1:** Across all four folds the slope of the 5-day excess return on the forecast is on the idea's side but small (slope 0.00032, day-clustered t 1.03, 3610 cases on 501 days), and its size is tiny: the unusual move is +0.21 % per case (t 0.73 over 1170 days), 0.010 of the coin's usual 12.04 % move, below the 0.22 % cost of a trade; the test already used every coin and every fold, so more data is not available.
- **F2:** In folds B and C the slope is near zero at every horizon (t −0.97 at 1 day, 0.55 at 3, 0.71 at 5, 0.63 at 10 and 0.49 at 20 days, about 1100 cases on 230 days).
- **F3:** The fall is not graded by thin volume. By forecast quintile, the 5-day excess return is −0.97 % (t −0.67) for the thinnest-volume quintile, −1.86 % (t −2.15) and −1.33 % (t −1.46) for the next two, and −0.22 % and −0.25 % for the heavy-volume quintiles. Within the thin-volume cases alone the slope is −0.00014 (t −0.11, 525 cases).
- **F4:** The slope does not settle on any part of the data. By year it runs from +0.0015 (t 1.24, 2018) to −0.0002 (t −0.13, 2021). By window it runs from +0.0020 (t 1.55, w7) to −0.0017 (t −1.00, w18). Coins split both ways: BTC +0.0016 (t 1.98), LINK −0.0047 (t −1.63), UNI −0.0068 (t −1.38).
- **F5:** What the bars do show is the decline itself, not its volume. Bars after a negative 28-day return are followed by a −1.19 % 5-day excess return (t −1.34, 835 cases) and −2.27 % over 10 days (t −1.70). Bars after a positive 28-day return are followed by +0.69 % and +1.17 %.
- **F6:** How deep the decline was is not graded either. By 28-day return quartile, the 5-day excess return is −0.46 % (t −0.22) for the deepest falls (mean −40 %), −2.83 % (t −2.60) for the next (−23 %), −1.93 % (t −1.63) for the next (−13 %) and +0.37 % for the shallowest (−5 %).
- **F7:** Calm declines and violent declines respond in opposite directions to how deep the fall was, but neither reading is clear. Calm means the 28-day mean daily range is below the coin's running usual range.

## Ideas
- No ideas: The volume-ratio effect is flat and ungraded in every part of the data I could see (F2–F4), the test already used all the data available (F1), and the only hint in the brief's direction (F7, calm declines continuing more the deeper they are) reaches t 1.57 at most, which is too weak to found an amended or new idea on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
