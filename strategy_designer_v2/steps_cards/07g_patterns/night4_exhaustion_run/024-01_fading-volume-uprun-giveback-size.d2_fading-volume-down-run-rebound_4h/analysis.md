---
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4044 USD
---
## Findings
- **F1:** The level of volume predicts the next 3 days. Cases were read once per 18-bar cell on each coin's grid. When a coin's 3-day mean log volume, against its 30-day norm, is in its top fifth, its unusual 18-bar move is +0.97 % (t 3.13, 1062 cases). In its bottom fifth it is −0.85 % (t −3.44, 1062 cases). The single-bar volume gives the same split: top fifth +1.02 % (t 3.23, strength 0.109), bottom fifth −0.60 % (t −2.64), 1059 cases each.
- **F2:** The high-volume effect is broad but not universal. Over years, the top volume fifth's unusual move is positive in 6 of 8: 2020 +2.50 % (t 2.98), 2023 +0.99 % (t 1.94), 2024 +2.18 % (t 2.06), 2025 +2.11 % (t 1.93), against 2018 −1.52 % (t −1.65). Over coins, it is positive in 5 of 6, from +0.16 % (BTC) to +2.38 % (XRP), with ETH at −0.28 %. Its +1.0 % per case is about 5 times the 0.19 % cost of a trade.
- **F3:** High volume after a fall is where the effect concentrates. In the top volume fifth, after a 1-day fall the unusual move is +1.38 % (t 3.16); after a 1-day rise it is +0.42 % (t 0.95). In the bottom volume fifth, after a fall it is −0.63 % (t −2.00). The rebound after falls therefore comes with rising volume, the opposite of the tested fading-volume situation.
- **F4:** The tested idea shows no edge. Its unusual move is +0.00 % (t 0.002, 4537 cases). Raw extremes do rebound: bottom fifth of the 1-day move +0.75 % (t 2.80), bottom fifth of the streak loss in usual moves +0.67 % (t 2.44). These are not graded, because the next fifth is −0.29 % and −0.75 % (t −3.09).
- **F5:** Active markets keep rising. The top fifth of 3-day realised activity (mean |return| against usual) gives +0.97 % (t 3.10), against −0.69 % (t −2.78) in the bottom fifth. The top fifth of bar range gives +0.78 % (t 2.43), against −0.67 % (t −2.97) in the bottom fifth. Both overlap with the volume effect: in the top activity fifth, the top volume fifth gives +1.75 %.
- **F6:** A large rise keeps going rather than giving back. The top fifth of the 3-day return in usual moves is followed by +0.98 % (t 3.34, 1059 cases), and by t 2.33 when volume is also in its top fifth. This contradicts the brief's give-back for rises.
- **F7:** Two calendar patterns stand out beyond the many angles looked at; both are ungraded, so they yield no idea under the rules:

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.g1_heavy-volume-precedes-rises` (from F1, F2, F5): The higher a coin's traded volume over the past 3 days relative to its own 30-day norm, the more the coin rises over the next 3 days, and the lower it is, the more the coin lags.
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.g2_high-volume-selloff-rebound` (from F3, F4, F1): After a coin's 1-day fall, the higher the volume of its latest 4-hour periods relative to its 30-day norm, the larger its rebound over the next 3 days.
- `024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound.g3_large-run-keeps-going` (from F6): The larger a coin's 3-day rise measured in its usual 4-hour moves over the past 30 days, the more it keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
