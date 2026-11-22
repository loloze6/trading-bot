---
line: 7.d not profitable
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h
idea tested: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3336 USD
---
## Findings
- **F1:** The book's gain before fees cannot pay its turnover: the summed bar gains are +10.58 against an estimated fee drag of 16.95 (turnover 30,818 × 0.00055). Over 49,416 trades, the mean trade gains +0.031 % before fees and loses −0.069 % after. This matches the idea's size: a total move of +0.05 % per case against a cost of 0.11 % per trade.
- **F2:** The trades entered at the capped forecast carry the loss. The 34,405 trades with an entry forecast of 10 to 20 average −0.027 % before fees and −0.127 % after. The 14,986 trades with an entry forecast of 2 to 10 average +0.15 % to +0.18 % before fees and +0.05 % to +0.08 % after.
- **F3:** Volume decides whether a fall rebounds. Among hours falling more than 2 typical moves, the 3-hour return is +0.20 % (t 4.21, n 1,915) in the third volume quartile and +0.17 % (t 2.73) in the top quartile, against +0.02 % (t 0.54) in the lowest.
- **F4:** On the non-overlapping 3-hour grid, the rebound covers the cost only on surging volume:
- **F5:** The rebound grows with the fall's depth, but only past several typical moves. The 3-hour return is +0.26 % (t 2.21, n 595) after falls deeper than 6 typical moves, about +0.10 % after falls of 2 to 4, and +0.035 % after falls of 1 to 1.5. Only the deepest bins exceed the 0.11 % cost.
- **F6:** The book is positioned away from the deep falls. It holds a mean position of 0.37 over the 64,967 up hours and turns over 9,344 units there, more than the 4,336 units turned over on falls deeper than 2 typical moves (7,662 bars). Those deep-fall bars still carry 3.85 of the book's 10.58 gross.
- **F7:** The rebound is absent in some years. The 3-hour return after falls deeper than 2 typical moves is +0.02 % in 2022 and −0.04 % in 2025, against +0.09 % to +0.23 % in the other years. The book's worst daily means fall in 2022 (−0.32 %) and 2025 (−0.25 %), with 2023 (−0.25 %) close behind on fees.

## Ideas
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound.d1_volume-surge-falls-rebound` (from F1, F2, F3, F4, F5, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its typical hourly volume over the past 30 days, the price recovers part of that fall over the next three hours. The larger that hour's volume against its 30-day typical volume, and the deeper the fall, the larger the recovery.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
