---
line: 7.g patterns
backtest: 012-01_liquidation-flush-rebound_1d
idea tested: 012-01_liquidation-flush-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3673 USD
---
## Findings
- **F1:** Volume alone carries the rebound after a fall. On the non-overlapping 3-day grid, down days (1-day return below 0) in the top volume-ratio quintile were followed by a mean 3-day excess return of +0.0180 (t 3.88, n 491). The other four quintiles were all negative, from −0.0013 to −0.0055 (|t| ≤ 1.49).
- **F2:** Among sharp falls (z < −1, n 623), the 3-day excess return rises with the volume ratio. The Spearman correlation is 0.133 (p 0.0008). The low-volume tercile gives −0.0137 (t −2.24, n 208) and the high-volume tercile gives +0.0256 (t 3.52, n 208).
- **F3:** The lower wick adds nothing and points the wrong way. Its Spearman correlation with the excess return among sharp falls is −0.066. In every volume tercile, falls with a long wick did worse than falls with a short wick: low volume −0.0247 (t −2.45) vs −0.0062, mid volume −0.0133 vs +0.0064, high volume +0.0226 vs +0.0303.
- **F4:** Quiet sharp falls tend to continue lower in most coins. Low-volume falls returned −0.033 in LTC (t −2.15), −0.035 in XRP (t −2.16) and −0.025 in ZEC (t −1.65). High-volume falls were positive in all six coins, and positive in every year from 2020 to 2025 (+0.019 to +0.067). They were negative in 2018 (−0.015) and 2019 (−0.003).
- **F5:** The volume effect is one-sided. Up days in the top volume-ratio quintile gave only +0.0008 (t 0.22, n 538), against +0.0180 for down days in the same quintile.
- **F6:** The coins rose on Saturdays: mean daily return +0.0045 (t 5.53, n 2484). It was positive in all six coins (t 1.40 to 2.92) and in 7 of 8 years; 2023 was flat at −0.00001. The book earned nothing on Saturdays (−0.00002, t −0.07).
- **F7:** The book barely beats holding. Its Sharpe is 0.557, only 0.003 above holding's Sharpe. Its mean daily return is +0.0004, and 2018 and 2022 were negative. The per-coin forecast ≥ 2 rebound was near zero in BTC (+0.0003) and ETH (+0.0015), and largest in ZEC (+0.029, t 2.74) and LTC (+0.015, t 2.09).

## Ideas
- `012-01_liquidation-flush-rebound.g1_volume-graded-fall-rebound` (from F1, F2, F3, F5, F7): After a day on which a coin closes lower, its return over the next 3 days is higher the larger that day's volume is relative to the coin's own 30-day average volume. It turns negative after falls on light volume, whatever the lower wick.
- `012-01_liquidation-flush-rebound.g2_quiet-falls-keep-falling` (from F2, F3, F4): After a sharp daily fall on volume below the coin's own 30-day average, the coin keeps falling over the next 3 days. The lighter the volume relative to that average, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
