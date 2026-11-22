---
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4710 USD
---
## Findings
- **F1:** The book's gain comes from long positions in rising coins (trending regime), while its shorts in falling coins lose. Per bar, trending longs earn a mean +0.168 % (t 4.45, 14645 bars, summed +24.6), and mean_reversion shorts lose a mean −0.106 % (t −3.15, 14294 bars, summed −15.2). Short trades entered in mean_reversion average −15.5 % net with a median of −10.1 % (t −19.0, 1907 trades), and they lose in every |entry forecast| quartile (−11.1 % to −17.3 %).
- **F2:** In coins up over 90 days, a day's rise is followed by a 5-day continuation that grows with the rise. The unusual 5-day move is −0.55 % after a 0–1 usual-move day (n 1046), +1.99 % after a 1–2 usual-move day (t 2.89, n 365) and +7.50 % after a rise above 2 usual moves (t 2.74, n 160). Across up days the rank correlation of rise size with the 5-day move is 0.12 (p 2e-6, n 1571). Rises above 2 usual moves are positive in both halves: +16.3 % (t 1.70, n 42) in 2018–21 and +4.38 % (t 3.05, n 118) in 2022–25.
- **F3:** In coins up over 90 days, a one-day fall is followed by a higher 20-day unusual move, larger the deeper the fall. The move is +12.2 % after a fall of 1–2 usual moves (t 3.18, n 82) and +13.1 % below −2 (n 11). By half, falls below −1 give +16.4 % (t 2.75, n 50) in 2018–21 and +7.6 % (t 2.53, n 43) in 2022–25. In both halves the order runs fall below −1 > fall of 0 to −1 > rise: +16.4/+8.3/+1.3 % and +7.6/+2.4/−2.4 %.
- **F4:** In coins down over 90 days, the fade of a bounce is not stable over time. After rises above 2 usual moves, the unusual 5-day move is −3.79 % overall (t −3.13, n 97), but +4.19 % in 2018–21 (t 2.23, n 24) against −6.41 % in 2022–25 (t −4.74, n 73). Only the modest 0–1 usual-move up days fade in both halves over 20 days: −6.28 % (t −2.22, n 55) and −6.09 % (t −3.68, n 134).
- **F5:** In coins down over 90 days, the 20-day fade is absent in the calmest third of each coin's volatility: −0.05 % (n 253) there, against −4.10 % (t −3.21, n 241) in the middle third and −3.49 % (t −2.66, n 222) in the highest. The book also lags holding the coins in 2021 and 2023: daily +0.085 % against +0.537 % in 2021, and −0.265 % against +0.323 % in 2023.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins.g1_dips-recover-in-rising-coins` (from F3, F1): In one coin up over its last 90 days, the deeper a one-day fall measured in usual daily moves (the day's return over the standard deviation of its last 20 daily returns), the higher its return over the next 20 days.
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins.g2_sharp-rises-extend-in-uptrends` (from F2, F1): In one coin up over its last 90 days, the larger a one-day rise measured in usual daily moves (the day's return over the standard deviation of its last 20 daily returns), the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
