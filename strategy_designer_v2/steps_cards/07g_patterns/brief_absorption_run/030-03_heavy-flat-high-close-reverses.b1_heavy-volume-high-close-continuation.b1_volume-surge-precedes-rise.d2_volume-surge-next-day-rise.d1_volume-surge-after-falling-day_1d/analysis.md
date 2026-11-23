---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3980 USD
---
## Findings
- **F1:** The rebound after a down day depends on how volatile the coin has been, not on its volume. In a regression of the next day's return (in usual daily moves) the term "fall × log(20-day volatility over its 120-day median)" has beta -0.278 with t -7.75. On days falling more than one usual move (z < -1), the next-day excess return by volatility tercile is +0.01 % (t -0.05, n 542), +0.61 % (t 2.23, n 366) and +1.48 % (t 4.05, n 302).
- **F2:** The high-volatility rebound after large falls holds up in every subset. It is positive in every year 2018–2025 (for example 2018 +2.23 % t 2.78; 2023 +1.90 % t 4.77; 2024 +0.73 % t 1.18). It is also positive in every coin, from +1.27 % for LTC to +1.88 % for ZEC, with BTC at t 2.53 and ZEC at t 2.14.
- **F3:** Once the fall's size, its interaction with volatility and the 5-day return are in the same regression, volume adds nothing. The tested interaction "fall × log volume ratio" has t -1.12, and log volume ratio alone has t 0.74. The volume-ratio quintile effect (top quintile +0.33 %, t 3.08) therefore looks like a stand-in for the size of the fall and for volatility.
- **F4:** The brief's close-location thesis has no information beyond the day's return. The close-location coefficient in the regression is 0.051 (t 0.89). On heavy-volume flat days the volume × close-location grid shows no consistent pattern: the top-volume row runs +1.07 %, -0.24 %, +0.51 %, +0.39 %, -0.75 %, all with |t| < 1.9.
- **F5:** A strong 5-day rise is followed by further gains. Its regression coefficient is 0.045 (t 3.37). On the non-overlapping 3-day grid, the top two deciles of the 5-day return earn +0.89 % (t 2.11) and +1.07 % (t 2.51) over the next 3 days, while deciles 1–7 sit between -0.16 % and -0.69 %. This is unstable by year: positive in 2020, 2021 and 2024 (t 2.66, 2.82, 3.21), negative in 2018, 2019, 2022 and 2023.
- **F6:** The book's worst 2 % of days (n 348) coincide with coin falls averaging -8.35 %, and its best 2 % with coin rises of +8.91 %. Its tails are the coin's own large moves while it is held long. This fits F1: long positions taken after falls in calm periods carry losses without the rebound.
- **F7:** A Thursday-plus-Friday next-day effect was strong in 2018–2019 (+0.91 %, t 3.37; +1.07 %, t 5.82) but faded to |t| < 1.9 from 2020 onwards. It is not a stable pattern and is not graded, so no idea is built on it.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound` (from F1, F2, F3, F6): The larger a coin's one-day fall, measured in its usual daily moves, the more it rises over the next day. The rebound grows with how high its 20-day volatility stands against its own level over the past 120 days, and it is largest when recent volatility is most elevated.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues` (from F5): The larger a coin's 5-day rise, measured in its usual 5-day moves, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
